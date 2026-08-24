# The pizza API on ECS Fargate

The Terraform that lessons 12, 13 and 14 of the `/terraform` track are written against.

It was **applied to a real AWS account, verified through the load balancer, and destroyed.** Every
output, timing and error quoted in those posts came from this stack running, not from
documentation.

```
                       internet
                          │
                   ┌──────▼──────┐
                   │     ALB     │  public subnets, 2 AZs, :80
                   └──────┬──────┘
                          │  :8085
                ┌─────────▼─────────┐
                │  ECS Fargate task │  private subnets
                │   pizza API       │
                └─────────┬─────────┘
                          │  :3306
                   ┌──────▼──────┐
                   │  RDS MySQL  │  private subnets
                   └─────────────┘

  NAT gateway (public subnet) ── outbound only: ECR pull, Secrets Manager, CloudWatch
```

## Layout

```
infra/
  versions.tf              provider constraints and default_tags
  main.tf                  wires the three modules together
  variables.tf outputs.tf
  modules/
    network/               VPC, 2 public + 2 private subnets, IGW, NAT, route tables
    database/              RDS MySQL, subnet group, security group
    service/               ECR, ECS cluster, task definition, service, ALB, IAM, logs
```

## Running it

⚠️ **This costs money while it is up** — about **$0.13/hour** in us-west-2:

| | hourly |
|---|---:|
| NAT gateway | $0.045 |
| ALB | $0.023 |
| Fargate 0.5 vCPU / 1 GB (ARM64) | $0.020 |
| RDS db.t4g.micro | $0.016 |
| **total** | **≈$0.13** |

Left running that is roughly **$92/month**. `terraform destroy` is not optional.

There is a chicken-and-egg problem on the very first apply: the ECS service references an image
that does not exist yet, in a repository that does not exist yet. So ECR is created first.

```bash
export AWS_PROFILE=folau
cd projects/terraform_tutorial/infra

terraform init

# 1. the registry, on its own. This is one of the few legitimate uses of -target,
#    which Terraform will warn you about and is right to.
terraform apply -target=module.service.aws_ecr_repository.this

# 2. build and push. NOTE --platform: see "Architecture" below.
cd ../../../lovemesomecoding_demo_project/pizza/pizza-springboot-backend
SHA=$(git rev-parse --short HEAD)
aws ecr get-login-password --region us-west-2 \
  | docker login --username AWS --password-stdin 329580012644.dkr.ecr.us-west-2.amazonaws.com
docker buildx build --platform linux/arm64 \
  -t 329580012644.dkr.ecr.us-west-2.amazonaws.com/pizza-tf:$SHA --push .

# 3. everything else
cd -
terraform apply -var "image_tag=$SHA"

curl "$(terraform output -raw app_url)/actuator/health/alb"

# 4. ⚠️ DO NOT SKIP
terraform destroy
```

## Architecture — read this before building the image

`cpu_architecture` defaults to **ARM64**, and the image must be built to match. A mismatch is not
caught at deploy time: the task starts, the kernel refuses the binary, and CloudWatch says
`exec /usr/bin/java: exec format error`.

ARM64 because Fargate on Graviton is ~20% cheaper, this is authored on an Apple Silicon Mac so the
build is **native**, and GitHub's free `ubuntu-24.04-arm` runners keep CI native too.

⚠️ **The x86 route from a Mac was tried first and does not work on this Dockerfile.**
`docker buildx build --platform linux/amd64` dies inside the Maven wrapper:

```
tar: apache-maven-3.9.16/lib/asm-9.9.1.jar: Cannot open: Function not implemented
tar: Exiting with failure status due to previous errors
```

That is QEMU's amd64 emulation missing a syscall GNU tar uses — nothing to do with the build. Going
x86 from an ARM machine needs either a `--platform=$BUILDPLATFORM` build stage or building the jar
on the host. Both work; neither is needed here.

Measured: the native arm64 build took **2m23s** end to end including the push.

## The health check path is not the obvious one

The ALB target group polls **`/actuator/health/alb`**, not `/actuator/health`.

`/actuator/health` aggregates every auto-configured indicator, and on this app it returns **503**
because the `jms` indicator cannot reach an Artemis broker that is not running and is not supposed
to be. An ALB reads 503 as unhealthy, kills the task, starts another, and the service cycles
forever with nothing in the logs that mentions health checks.

`/actuator/health/alb` is a health *group* containing only `ping`. See the demo app's
`application.properties`, and `SecurityConfig.java` — which had to be widened to
`/actuator/health/**`, because permitting the exact string `/actuator/health` left the group
returning 403.

## What is deliberately not here

- **No HTTPS.** The listener is plain HTTP on :80. Real TLS needs an ACM certificate, which needs a
  domain, which is beyond what these lessons are about. Post 15 says so plainly rather than
  implying the stack is production-ready.
- **No remote state.** This root module uses local state, so the lessons can be followed without
  first creating a bucket. Lesson 8 covers the S3 backend and `use_lockfile`, and moving this stack
  onto it is a `backend` block plus `terraform init -migrate-state`.
- **No autoscaling, no multi-AZ RDS, no second NAT gateway.** Each is a deliberate cost trade and
  each is commented where it is made.

## Teardown

```bash
terraform destroy
```

Then confirm nothing survived — everything carries `Project=terraform-tutorial`, which is what
makes this query trustworthy:

```bash
aws resourcegroupstaggingapi get-resources \
  --tag-filters Key=Project,Values=terraform-tutorial \
  --region us-west-2 --query 'ResourceTagMappingList[].ResourceARN'
```

⚠️ The account holds three **unrelated** ECS clusters — `learnmymath-api`, `development`,
`pocsoft`. Never tear down by resource type; always by tag or by the `pizza-tf` prefix.
