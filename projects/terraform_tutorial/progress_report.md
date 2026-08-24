# Terraform tutorial track — progress report

**Status:** ✅ **LIVE.** All 16 posts published at https://lovemesomecoding.com/terraform (2026-08-24, build `394b0bd`).
**Started:** 2026-08-24
**Where it lands:** https://lovemesomecoding.com/terraform

---

## What is there now

3 published posts, measured off the **prod** content tree. No drafts. No redirects touch
`/terraform`.

| slug | date | prose words | code | headings | imgs |
|---|---|---:|---:|---:|---:|
| `terraform-introduction` | 2019-07-09 | 54 | 0 | 0 | 0 |
| `terraform-with-aws` | 2019-07-09 | **2** | 0 | 0 | 0 |
| `terraform-fundamentals` | 2019-07-09 | **2** | 0 | 0 | 0 |
| **total** | | **58** | **0** | **0** | **0** |

### The defects

1. **Two of the three posts are the literal string "Coming soon…".** `terraform-with-aws` and
   `terraform-fundamentals` are `status: published` and have been serving that since 2019, last
   touched 2021-10-11.

2. **The third is copied HashiCorp marketing blurb.** `terraform-introduction` opens with the
   verbatim "Terraform is an infrastructure as code (IaC) tool that allows you to build, change,
   and version infrastructure safely and efficiently…" paragraph from the product page. 54 words,
   then it stops. Duplicate content against developer.hashicorp.com, and the opposite of what
   CLAUDE.md says this site is for.

3. **WordPress `boldgrid-section` / `container` / `row` / `col-md-12` wrappers** on all three —
   dead Bootstrap markup from the old theme. `terraform-with-aws` has them nested twice.

4. **Zero headings, so `toc` is empty on all three.** No table of contents, no deep links.

5. **The category record is broken** — `{"slug": "terraform", "name": "terraform",
   "description": ""}`. Lowercase name, no standfirst on the archive page.

This is the emptiest track on the site. Effectively it is being written from nothing, not
rewritten.

### The slugs are frozen

All 3 are live, indexed URLs. `scripts/verify-build.mjs` check 1 fails the frontend build if any
URL in `index/posts.json` stops resolving, so all three are **rewritten in place** and keep their
slugs. The 13 new posts are additive.

Dates are sticky — `upsert_post` never overwrites an existing date, and all three already carry
2019-07-09. Getting them to read first in a 2026 track therefore needs `--force-dates` **once**.
See "The `--force-dates` decision" below; this track follows the FastAPI correction, not the
Docker one.

### Navigation — nothing to do

`lovemesomecoding_frontend/src/lib/nav.ts:28` already lists `terraform` in the **DevOps** group and
`:52` maps it to the display name `Terraform`. Only the stored category record needs fixing, via
`upsert_category`.

---

## Sources

From the README:

- https://developer.hashicorp.com/terraform/tutorials — the official learning track
- https://www.tutorialspoint.com/devops/devops-terraform.htm — named in the README as a topic
  source. Treated as a *topic list only*; it is written against Terraform 0.11-era syntax and its
  examples are not quotable.
- https://registry.terraform.io/providers/hashicorp/aws/latest/docs — the authority on every
  resource argument actually used here
- `lovemesomecoding_demo_project/pizza/pizza-springboot-backend` — the app that gets deployed,
  per the README. This is the part that is genuinely first-hand.

Filter, from the README: *"We don't need to create a post for each small things. We just need the
most important topics to cover."* and *"keep posts to the point."*

---

## Versions this track is written against

Read off this machine, not chosen from documentation.

| | |
|---|---|
| Terraform | **1.15.9** (`~/bin/terraform`, installed 2026-08-24) |
| AWS provider | **6.61.0** (`hashicorp/aws`, published 2026-08-19) |
| AWS CLI | 2.32.24 |
| Account / region | `329580012644` / `us-west-2` |
| Demo app | Java 21, Spring Boot 4.1.0, MySQL 8.4 |

⚠️ **Homebrew could not do this upgrade.** `brew upgrade terraform` fails on this machine with
`Error: Your Xcode (15.4) at /Applications/Xcode.app is too outdated` — an Xcode check unrelated to
Terraform, which is a single static Go binary. It was installed instead by downloading the official
release, verifying it against HashiCorp's published `SHA256SUMS`, and dropping it in `~/bin`, which
is first on `PATH` and therefore shadows Homebrew's 1.9.5 at `/opt/homebrew/bin/terraform`.

To undo: `rm ~/bin/terraform`. To re-do after a Homebrew Terraform upgrade ever succeeds, delete
`~/bin/terraform` so the Cellar one wins again. **Do not spend time on `brew upgrade terraform`
again** — the blocker is Xcode, not Terraform, and updating Xcode is a multi-gigabyte App Store
download for no benefit here.

### Two things that make 2019 Terraform content actively wrong

**The license changed.** HashiCorp moved Terraform from MPL 2.0 to the Business Source License on
2023-08-10. The Linux Foundation forked the last MPL commit as **OpenTofu**, which is now a CNCF
project and a drop-in for most usage. Any tutorial written before August 2023 describes Terraform
as open source without qualification, and that is no longer true. This track states the position
once, in lesson 1, and does not editorialise further.

**DynamoDB state locking is no longer how you do it.** Every S3-backend tutorial on the internet
tells you to create a DynamoDB table with a `LockID` primary key. Terraform 1.10 added native S3
locking via a `.tflock` object, and **1.11 promoted it to the default and deprecated
`dynamodb_table`**, which now emits a warning and is slated for removal. Lesson 8 uses
`use_lockfile = true` and mentions the DynamoDB table only to say why you will see it everywhere
and should not copy it. This is the single most commonly-stale piece of Terraform advice.

---

## The track — 16 posts

3 rewritten in place, 13 new. Sized to match the FastAPI and Postgres tracks. Reading order is
publish order; dates are computed from `START_DATE` in `manifest.py`.

| # | slug | state | what it covers |
|---:|---|---|---|
| 1 | `terraform-introduction` | rewrite | What IaC solves, Terraform vs CloudFormation/CDK/Pulumi/Ansible, the BSL change and OpenTofu, the versions above, the demo app, full lesson index |
| 2 | `terraform-fundamentals` | rewrite | Install, the `init` → `plan` → `apply` → `destroy` loop, a first real resource, what each command actually does |
| 3 | `terraform-hcl-syntax` | new | Blocks, arguments, types, expressions, functions, `fmt`, `console` |
| 4 | `terraform-providers` | new | `required_providers`, version constraints, `.terraform.lock.hcl`, provider config, aliases, multi-region |
| 5 | `terraform-resources-and-state` | new | What state *is* and why it exists, addressing, implicit vs explicit dependencies, `lifecycle`, `state` subcommands, `-replace` |
| 6 | `terraform-variables-and-outputs` | new | Types, `validation`, `sensitive`, `.tfvars`, precedence order, locals, outputs |
| 7 | `terraform-data-sources` | new | Reading what you did not create, `aws_ami`, `aws_availability_zones`, data vs resource |
| 8 | `terraform-remote-state` | new | S3 backend, **native `use_lockfile` locking**, bootstrapping the bucket, why local state fails the moment there are two of you |
| 9 | `terraform-loops-and-conditionals` | new | `count` vs `for_each` and when each is wrong, `for` expressions, `dynamic` blocks, splat |
| 10 | `terraform-modules` | new | Structure, inputs/outputs, calling local and registry modules, versioning, when *not* to write one |
| 11 | `terraform-environments-and-workspaces` | new | Workspaces vs directories vs tfvars, what actually scales past two environments |
| 12 | `terraform-with-aws` | rewrite | **ECS part 1** — VPC, subnets, security groups, RDS MySQL for the pizza API |
| 13 | `terraform-ecs-fargate-deploy` | new | **ECS part 2** — ECR, task definition, Fargate service, ALB, target group, health checks, CloudWatch logs |
| 14 | `terraform-github-actions-cicd` | new | OIDC (no stored AWS keys), plan-on-PR, apply-on-merge, build and push to ECR, `force-new-deployment` |
| 15 | `terraform-production-practices` | new | Least privilege, `prevent_destroy`, drift, reviewing a plan, cost, secrets in SSM, `moved`/`import`, `terraform test` |
| 16 | `terraform-interview-questions` | new | The questions Terraform interviews actually ask |

Posts 12–14 are the README's centrepiece requirement and are written against a stack that is
**actually applied to AWS**, not just planned. See below.

---

## The ECS deploy — decisions

The README asks for a script that deploys `pizza-springboot-backend` to ECS with a GitHub Actions
CI/CD pipeline, and for that script to become the worked example.

**Decision (2026-08-24, confirmed with Folau): apply it for real, verify, then destroy.** Every
output, ARN, timing and dollar figure quoted in posts 12–14 is measured against a stack that ran,
in the same spirit as the Docker track building and running every image before quoting it. The
stack is then destroyed — it is not left standing. Rough cost of a few hours up: ALB $0.022/hr,
Fargate 0.5vCPU/1GB ~$0.02/hr, NAT $0.045/hr, RDS db.t4g.micro ~$0.016/hr — call it well under $1.

Rejected: leaving it running (~$60-70/month against a site that costs $0.60/month), and
plan-only (the README wants a script that demonstrably works).

### Account shape it has to fit into

| | |
|---|---|
| Account | `329580012644`, user `folauk110` |
| Region | us-west-2 |
| VPCs | **only the default**, `vpc-60d8ba18` (172.31.0.0/16) |
| Existing ECS clusters | `learnmymath-api`, `development`, `pocsoft` — all unrelated legacy, **do not touch** |
| Terraform state bucket | **does not exist yet** — lesson 8 creates it |

The track builds its **own** VPC rather than using the default. Building a VPC is most of what a
real Terraform AWS tutorial is for, and reusing the default would skip subnets, routing and
gateways entirely.

⚠️ **Everything this track creates gets a `pizza-tf` name prefix and a
`Project = "terraform-tutorial"` tag**, so `destroy` is provably complete and nothing collides
with the three legacy clusters.

### The NAT gateway question

Tasks in private subnets need a NAT gateway to pull from ECR — $0.045/hr, ~$32/month, and the
single most common surprise bill in every ECS tutorial. The alternatives are public subnets with
`assign_public_ip = true` (free, less correct) or VPC interface endpoints (cheaper at rest, more
HCL). Post 13 builds the private-subnet + NAT version because it is the right shape, and states
the cost plainly with both alternatives named. Not resolved yet whether the applied stack uses NAT
or endpoints — decide when writing post 13.

### The demo app needed three changes — ✅ DONE

`SecurityConfig.java` already permitted `/actuator/health`, but **`spring-boot-starter-actuator`
was not in `pom.xml`**, so that path returned 404. An ALB target group needs a health check that
returns 200 without a JWT, and it **kills a task whose health check fails** — so this had to be
right before any infrastructure was built on top of it.

Getting there turned up two traps that only appear when you actually run it. Both are measured on
this machine, both are worth a section in post 13, and neither is visible from reading the code.

**1. `/actuator/health` returns 503, not 200.** Adding the starter is not enough. Boot
auto-configures a health indicator for every optional dependency on the classpath and aggregates
them all into one status:

```
GET /actuator/health  ->  503  {"status":"DOWN"}
  jms            DOWN   jakarta.jms.JMSException: Failed to create session factory
  elasticsearch  UP     ... but only by accident, see below
  diskSpace      UP
```

`jms` is DOWN because Artemis is not running — it is not meant to be, and it has nothing to do with
whether the JVM can serve an HTTP request. Point an ALB at that and **every task fails its health
check, gets killed, gets replaced, and fails again**: the service never stabilises and the symptom
looks like a networking problem.

Worse, `elasticsearch` reported UP only because **another project's** container
(`stayhub-elasticsearch`) happens to be on `localhost:9200`. On ECS neither dependency exists, so
both would have been DOWN.

The fix is a health **group**, which is a whitelist rather than a blacklist:

```properties
management.endpoint.health.group.alb.include=ping
```

Disabling the failing indicators one at a time works today and silently breaks the next time
somebody adds a starter. `ping` is UP whenever the context is serving — exactly the question the
load balancer is asking. The ungrouped `/actuator/health` keeps every indicator and is what
*monitoring* should read: monitoring pages a human, it does not delete your capacity.

**2. The group was then 403.** `SecurityConfig` permitted the exact string `/actuator/health`, so
`/actuator/health/alb` fell through to `.anyRequest().authenticated()`. An ALB reads 403 as
unhealthy, so this would have produced the identical cycling failure. It is now
`"/actuator/health", "/actuator/health/**"`.

Verified on the running app:

```
GET /actuator/health/alb   ->  200  {"status":"UP"}      <- the ALB target group polls this
GET /actuator/health       ->  503  {"status":"DOWN"}    <- the truth, for monitoring
GET /actuator/env          ->  403   (configprops, beans, metrics, heapdump: all 403)
```

⚠️ **The ALB health check path is `/actuator/health/alb`, not `/actuator/health`.** Post 13 and the
`infra/` service module must both use it.

**Test suite:** 3 failures — `ReportServiceImplTest` (×2) and
`CustomerOrderDAOIntegrationTest.filtersByStatus`. All three **pre-date this work**: verified by
`git stash`ing the changes and reproducing each one identically on the clean tree. They assert
absolute row counts (`expected: 2 but was: 23`) against the shared, accumulating dev MySQL, which
has months of Playwright fixtures in it. Not caused here and not fixed here — but worth knowing
they are red independently of this track. `spotless:apply` run, no further changes.

---

## The applied run — 2026-08-24

The stack in `infra/` was **applied to account 329580012644, verified through the load balancer,
and destroyed.** This section is the evidence, because posts 12-14 quote it.

| | |
|---|---|
| Resources created | **38** (31 carrying the Project tag) |
| ALB | `http://pizza-tf-1743134304.us-west-2.elb.amazonaws.com` |
| RDS creation time | **5m17s** — by far the long pole in the apply |
| Task | Fargate **ARM64**, 512 CPU / 1024 MB, revision 2 |
| Image build | native arm64, **2m23s** including push |
| Cost | up ~50 minutes, ≈ **$0.11** |

Verified through the load balancer, not from the configuration:

```
GET /actuator/health/alb   -> 200  {"status":"UP"}
GET /api/products          -> 200  14 products, served from MySQL on RDS
GET /api/admin/users       -> 403  (no token — security intact through the ALB)
```

The 14 products prove more than routing: Liquibase ran its migrations, which means the task
resolved its database credentials out of Secrets Manager and connected. That is the whole secrets
path working, proven by data rather than by a log line.

### The password really is not in the state file

The claim in `modules/database/main.tf` is the module's main teaching point, so it was checked
rather than asserted — pull the live password from Secrets Manager and grep the state for it:

```
password length: 28 chars
✓ NOT in terraform.tfstate

aws_db_instance attributes actually stored:
  password:                    null
  manage_master_user_password: true
  master_user_secret:          [{ secret_arn: "arn:aws:se…", kms_key_id: "…" }]
```

And the honest counterpart, also verified: `random_password.result` **is** in state, exactly as the
comment in `modules/service/main.tf` says. `random_password` stores its output by definition. The
genuinely state-free pattern is the RDS one — have AWS generate and own the value, and only ever
reference its ARN.

### Three things broke, and all three are content

**1. `docker buildx --platform linux/amd64` fails outright on this Mac.**

```
tar: apache-maven-3.9.16/lib/asm-9.9.1.jar: Cannot open: Function not implemented
tar: Exiting with failure status due to previous errors
```

QEMU's amd64 emulation is missing a syscall GNU tar uses, inside the Maven wrapper's own
bootstrap. Nothing to do with the Dockerfile. **Resolution:** the track went ARM64 — Graviton
Fargate is ~20% cheaper, the build is native on Apple Silicon (2m23s), the demo app's Dockerfile
needs no changes, and GitHub's free `ubuntu-24.04-arm` runners keep CI native too.
`cpu_architecture` is a variable, and `runtime_platform` is stated explicitly rather than
defaulted, because a mismatch is not caught at deploy time — the task just dies with
`exec format error`.

⚠️ This also resolves the open question about the build: **do not try to cross-build x86 from this
machine on this Dockerfile.** It needs a `--platform=$BUILDPLATFORM` build stage or a host-built
jar, and neither is necessary.

**2. The first apply cycled tasks forever.** The target group flipped `initial` → `draining` →
`initial` indefinitely and the ECS service events said only "registered 1 targets" / "has started 1
tasks". `stopCode` was `EssentialContainerExited`, exit 1. The reason was only ever in CloudWatch:

```
Property: pizza.cors.allowedOrigins
Value: "[]"
Reason: must not be empty
```

`PizzaProperties` declares `Cors(@NotEmpty List<String> allowedOrigins)`, and the module passed an
empty string. **Resolution:** default it to `http://${aws_lb.this.dns_name}` — non-empty, and
genuinely correct, since that is the origin the API is served from. Referencing the ALB from the
task definition is not a cycle; the load balancer does not depend on the task definition.

This is the single most useful debugging lesson in the track: **the ECS console tells you the task
stopped, never why.** The exit code is in `describe-tasks`, and the cause is in the log group.

**3. `hcl` was not a supported code language on this site.** Every HCL block in all 16 posts would
have rendered as unhighlighted plaintext — silently, because `normalize_language()` normalises an
unknown language rather than rejecting it. Fixed in lockstep, which is what the frontend file's own
comment demands:

- `lovemesomecoding_backend/app/services/content.py` — added `hcl` to `SUPPORTED_LANGUAGES`, plus
  aliases `terraform` → `hcl` and `tf` → `hcl`, since HashiCorp's docs and most editors say
  "terraform" where Prism says "hcl".
- `lovemesomecoding_frontend/src/lib/content.ts` — added the static
  `import 'prismjs/components/prism-hcl'`. Prism ships the grammar; a `language-hcl` class with no
  grammar behind it highlights as nothing at build time.

Backend suite after the change: **90 passed, 95% coverage.**

### Teardown — confirmed clean

`terraform destroy` reported **40 destroyed**, and every billable thing was then checked by name
rather than trusted:

```
RDS pizza-tf-mysql   DBInstanceNotFound
NAT gateways         0 available   (nat-050abac836d239a9e -> deleted)
Load balancers       0 named pizza-tf
Elastic IPs          0
ECR pizza-tf         RepositoryNotFoundException
ECS cluster pizza-tf INACTIVE
task definitions     0 ACTIVE
```

The three pre-existing clusters — `learnmymath-api`, `development`, `pocsoft` — are untouched.

⚠️ **The Resource Groups Tagging API lies for a while after a destroy.** It still listed the ECS
cluster, the service, the NAT gateway and several security group rules minutes after all of them
were gone. It is an index, and it lags. Verify teardown per-service, by name — a tag query is
useful for *finding* things, not for proving their absence.

(Deregistered task definitions stay visible as INACTIVE forever by design. They are not billable.)

---

## Tooling — what verifies this track

Copied from `projects/docker_tutorial/`, which is the closest analogue (DevOps, same demo app).

```
projects/terraform_tutorial/
  manifest.py           category metadata + one entry per post
  posts/NN-slug.html    post bodies, plain semantic HTML
  seed.py               writes the category and posts into a content tree
  check_content.py      the HTML round-trips; length/prose/safety rules
  check_hcl.py          NEW — every quoted HCL block is real Terraform
  check_snippets.py     every quoted snippet still matches the demo app
  verify_rendered.mjs   drives a browser at the built site
  infra/                the actual ECS Terraform, applied and destroyed
```

**`check_hcl.py` is this track's `check_aws.py`.** Every `hcl`/`terraform` code block gets written
to a temp module and run through `terraform fmt -check` and `terraform init -backend=false &&
terraform validate` — which proves the syntax parses, the provider has the resource, **and every
argument is a real argument of that resource**, offline against the downloaded provider schema, no
credentials, nothing billed. That is exactly how old Terraform content rots: a renamed argument, a
removed one, a resource that moved.

What it will NOT prove, stated plainly so nobody trusts it further than it goes:
- Not that `apply` succeeds — no quota, permission or account state is consulted.
- Not that argument *values* are valid. `instance_type = "banana"` passes validate.
- Blocks that are deliberate fragments need marking as such rather than being validated whole.

---

## The `--force-dates` decision

All three existing slugs carry 2019-07-09. Without `--force-dates` they keep it, sort to the back
of a 2026 track, and lessons 1, 2 and 12 read *last* — which is exactly backwards.

So `--force-dates` is needed on the **first** prod publish. Per the correction the FastAPI track
established, this is **not** treated as a one-off to be documented and then forbidden; it is
whatever a manifest date change requires. Dates here are *computed* from `START_DATE`, so a
re-base is an intended operation, unlike the AWS track where dates are transcribed from a
published archive and must never move.

---

## Progress

| stage | what | state |
|---|---|---|
| 0 | survey, decisions, this document | ✅ done |
| 1 | `manifest.py`, `seed.py`, `check_content.py` scaffolding | ✅ done |
| 2 | `infra/` — write, apply, verify, destroy the ECS stack | ✅ done |
| 3 | actuator + health group added to the demo app | ✅ done |
| 4 | `check_hcl.py` + `tests/test_check_hcl.py` | ✅ done |
| 5 | `hcl` added as a highlighted language (backend + frontend) | ✅ done |
| 6 | posts 1–16 | ✅ done |
| 7 | seed `local`, build, verify rendering | ✅ done |
| 8 | seed `prod` (with `--force-dates`), deploy | ✅ done |

**LIVE.** 16 posts at `/terraform`, 21,116 words, 190 code blocks, dated 2026-07-10 → 2026-08-24.

```
check_content.py    16/16 written, every code sample round-trips byte-for-byte
check_hcl.py        86 HCL blocks: 62 validated, 23 fragment, 1 lock file, 0 failed
check_hcl --infra   infra/ validates and is formatted
test_check_hcl.py   catches every planted error, passes every honest fragment
backend pytest      90 passed, 95% coverage
npm run deploy      735/735 posts served, edge verified on build 394b0bd
```

All 16 URLs return 200 in production. The three frozen slugs kept their URLs and now carry
1,462 / 1,568 / 1,770 words in place of 54 / 2 / 2. HCL renders Prism-highlighted live.

⚠️ **`--force-dates` has now been used** on the prod publish, to move the three 2019 posts into
reading order. Dates here are computed from `START_DATE`, so re-basing remains an intended
operation — but a routine correction is `seed.py --env prod --write` with no flag, followed by
`npm run deploy`.

---

## If you come back to this

### Next session starts here

1. Run **both** checks before any edit ships. `check_content.py` proves the HTML round-trips;
   `check_hcl.py` proves the Terraform is still real against the pinned provider. Only the second
   goes stale on its own — a provider release renaming an argument does not disturb the HTML.
2. `check_hcl.py` treats a **deprecation warning as a failure**. That is deliberate: shipping
   syntax that still works but should no longer be taught is exactly what dates a tutorial.
3. Post 1 carries the lesson index and `check_content.py` fails if a manifest lesson is not linked
   from it, so adding a post means editing that index.
4. Posts 12–14 quote `infra/`. Do not re-apply to edit them — the measurements are in "The applied
   run" above. Re-apply only if `infra/` itself changes, and destroy afterwards.

---

## Open questions

- **Post 14's pipeline cannot be proven.** `lovemesomecoding_demo_project` still has no GitHub
  remote, so a workflow written for it has never run — the same caveat the Docker track's
  `docker.yml` carries and states openly. Post 14 must say so rather than implying it was
  exercised. The OIDC trust policy and the IAM role can still be written and `validate`d.
- **HTTPS is out of scope and the posts must say so.** The listener is plain HTTP on :80; real TLS
  needs an ACM certificate and a domain. Post 15 should name this as the first thing to add rather
  than leaving the stack looking production-ready.

### Resolved

- ~~NAT gateway or VPC interface endpoints?~~ **NAT gateway**, one, in a public subnet. Five
  interface endpoints are needed to run Fargate privately at ~$0.01/hr each — more than one NAT
  gateway's $0.045/hr until data volume is high. Both alternatives are named in
  `modules/network/main.tf` where the trade is made.
- ~~RDS or a MySQL container?~~ **RDS**, `db.t4g.micro`. It is the honest answer and the whole run
  cost about $0.11.
- ~~x86 or ARM?~~ **ARM64.** Cross-building x86 from this Mac fails outright in QEMU; see "Three
  things broke" above.
