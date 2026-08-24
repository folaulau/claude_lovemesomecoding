# The pizza API on ECS Fargate, behind an application load balancer.
#
# Quoted by lesson 13 of the /terraform track on lovemesomecoding.com.
#
#   internet -> ALB (public subnets, :80) -> target group -> task (private, :8085)
#
# The task has no public address. The only way to reach it is through the load
# balancer, which is the only thing in this module with an internet route.

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

# --------------------------------------------------------------------- ECR
resource "aws_ecr_repository" "this" {
  name = var.name_prefix

  # Tags become immutable: pushing `:abc123` twice is then an error rather than
  # silently moving the tag. It is what makes "which image is running?" a
  # question with an answer, and it is why the pipeline tags by git SHA rather
  # than reusing :latest.
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  # So `terraform destroy` works. Default is false, and ECR refuses to delete a
  # repository that still has images in it - which it always will by then.
  force_delete = true

  tags = merge(var.tags, { Name = var.name_prefix })
}

# Untagged layers accumulate on every rebuild and are billed per GB. This expires
# them after a day; without it a busy pipeline quietly grows a storage bill.
resource "aws_ecr_lifecycle_policy" "this" {
  repository = aws_ecr_repository.this.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Expire untagged images after 1 day"
      selection = {
        tagStatus   = "untagged"
        countType   = "sinceImagePushed"
        countUnit   = "days"
        countNumber = 1
      }
      action = { type = "expire" }
    }]
  })
}

# ------------------------------------------------------------------- logs
resource "aws_cloudwatch_log_group" "this" {
  name = "/ecs/${var.name_prefix}"

  # Logs are billed for storage forever by default (retention_in_days unset means
  # "never expire"). On a demo stack that is a bill with no end date.
  retention_in_days = var.log_retention_days

  tags = var.tags
}

# ------------------------------------------------------------------ secrets
#
# The JWT signing key. `random_password` generates it, so no human ever picks it
# and it is not in the source.
#
# ⚠️ Honest caveat: unlike the RDS master password, THIS value IS in the
# Terraform state file. random_password stores its result in state by definition -
# that is how it stays stable across applies. Marking it sensitive hides it from
# output, not from the file.
#
# That is acceptable here because the state bucket is encrypted and private, and
# because it is the trade every `random_password` makes. The genuinely
# state-free pattern is the RDS one in the database module: have AWS generate and
# own the value, and only ever reference its ARN.
resource "random_password" "jwt" {
  length = 64
  # No punctuation. The value reaches the app through an environment variable and
  # a shell-quoting bug in anything along the way turns a $ or a ` into a silent
  # truncation. 64 alphanumeric characters is ~380 bits; the special characters
  # buy nothing here.
  special = false
}

resource "aws_secretsmanager_secret" "jwt" {
  name = "${var.name_prefix}/jwt-secret"

  # ⚠️ Secrets Manager does NOT delete immediately - it schedules deletion, with a
  # 30-day recovery window by default. A destroy followed by an apply then fails
  # with "already scheduled for deletion", because the name is still taken. Zero
  # forces immediate deletion, which is what a stack that gets torn down and
  # rebuilt needs.
  recovery_window_in_days = 0

  tags = var.tags
}

resource "aws_secretsmanager_secret_version" "jwt" {
  secret_id     = aws_secretsmanager_secret.jwt.id
  secret_string = random_password.jwt.result
}

# -------------------------------------------------------------------- IAM
#
# TWO roles, and the distinction matters:
#
#   execution role - assumed by the ECS AGENT, before your container starts. It
#                    pulls the image, fetches secrets and creates log streams.
#   task role      - assumed by YOUR CODE, once it is running. It is what the AWS
#                    SDK inside the application picks up.
#
# Giving the application the execution role's permissions is a common shortcut
# and it hands your code the ability to read every secret the task uses.

data "aws_iam_policy_document" "ecs_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "execution" {
  name               = "${var.name_prefix}-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
  tags               = var.tags
}

# The AWS-managed policy covering ECR pull and CloudWatch Logs write.
resource "aws_iam_role_policy_attachment" "execution_managed" {
  role       = aws_iam_role.execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Reading the secrets is NOT in that managed policy, and its absence is one of
# the most confusing ECS failures there is: the task stops during provisioning
# with ResourceInitializationError and the application logs are empty, because
# the container never started.
#
# Scoped to exactly these two secret ARNs rather than "*".
data "aws_iam_policy_document" "execution_secrets" {
  statement {
    actions = ["secretsmanager:GetSecretValue"]
    resources = [
      aws_secretsmanager_secret.jwt.arn,
      var.db_secret_arn,
    ]
  }
}

resource "aws_iam_role_policy" "execution_secrets" {
  name   = "${var.name_prefix}-secrets"
  role   = aws_iam_role.execution.id
  policy = data.aws_iam_policy_document.execution_secrets.json
}

# The task role carries NO policies. The pizza API does not call AWS at all, so
# an empty role is the correct amount of permission. It exists because giving a
# task no role at all makes it fall back in ways that are harder to reason about
# than an explicitly empty one.
resource "aws_iam_role" "task" {
  name               = "${var.name_prefix}-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
  tags               = var.tags
}

# --------------------------------------------------------- load balancer
resource "aws_security_group" "alb" {
  name        = "${var.name_prefix}-alb"
  description = "Public HTTP to the load balancer"
  vpc_id      = var.vpc_id
  tags        = merge(var.tags, { Name = "${var.name_prefix}-alb" })
}

resource "aws_vpc_security_group_ingress_rule" "alb_http" {
  security_group_id = aws_security_group.alb.id
  description       = "HTTP from anywhere"
  from_port         = 80
  to_port           = 80
  ip_protocol       = "tcp"
  cidr_ipv4         = "0.0.0.0/0"
}

# The ALB must be able to reach the tasks. Without an egress rule it cannot, and
# every target reports unhealthy with no explanation on either side.
resource "aws_vpc_security_group_egress_rule" "alb_to_tasks" {
  security_group_id            = aws_security_group.alb.id
  description                  = "To the application tasks"
  from_port                    = var.container_port
  to_port                      = var.container_port
  ip_protocol                  = "tcp"
  referenced_security_group_id = var.app_security_group_id
}

resource "aws_lb" "this" {
  name               = var.name_prefix
  load_balancer_type = "application"
  internal           = false
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  tags = merge(var.tags, { Name = var.name_prefix })
}

resource "aws_lb_target_group" "this" {
  name = var.name_prefix
  port = var.container_port

  # HTTP between the load balancer and the task, inside the VPC. TLS terminates
  # at the ALB. Encrypting this hop too is a real production question; it is not
  # what makes a public endpoint HTTPS.
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  # ⚠️ "ip", not "instance". Fargate tasks use awsvpc networking and each gets
  # its own ENI and private IP - there is no EC2 instance to register. With
  # "instance" the service fails to register targets at all.
  target_type = "ip"

  health_check {
    enabled = true

    # ⚠️ /actuator/health/alb, NOT /actuator/health.
    #
    # Plain /actuator/health aggregates every auto-configured indicator and
    # returns 503 whenever any optional dependency is unreachable - measured on
    # this app, `jms` is DOWN because Artemis is not running and is not meant to
    # be. The ALB would read that as unhealthy, kill the task, start another, and
    # cycle forever with no error that mentions health checks.
    #
    # `/actuator/health/alb` is a health GROUP containing only `ping`, which is
    # UP whenever the JVM is serving. See application.properties in the demo app.
    path                = var.health_check_path
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }

  # A Spring Boot app on Fargate takes a while to boot and start serving. The
  # deregistration delay is separate: it is how long the ALB waits for in-flight
  # requests before removing a draining target. The default 300s makes every
  # deploy take five minutes longer than it needs to.
  deregistration_delay = 30

  tags = var.tags
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }
}

# ------------------------------------------------------------------- ECS
resource "aws_ecs_cluster" "this" {
  name = var.name_prefix
  tags = merge(var.tags, { Name = var.name_prefix })
}

resource "aws_ecs_task_definition" "this" {
  family = var.name_prefix

  # Fargate requires awsvpc, and requires cpu/memory at the TASK level. The valid
  # pairings are fixed: 512 CPU units (0.5 vCPU) allows 1024-4096 MB and nothing
  # else. An invalid pair is rejected at apply time with a clear message, which is
  # one of the friendlier AWS validations.
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.task_cpu
  memory                   = var.task_memory

  execution_role_arn = aws_iam_role.execution.arn
  task_role_arn      = aws_iam_role.task.arn

  # ⚠️ STATED EXPLICITLY, because the default is X86_64 and the machine this was
  # authored on is Apple Silicon.
  #
  # An image built on an arm64 Mac and run on an X86_64 task starts, fails
  # immediately, and the only clue in CloudWatch is:
  #
  #     exec /usr/bin/java: exec format error
  #
  # ECS does not check the architecture at deploy time; it finds out when the
  # kernel refuses the binary. So `docker build` on a Mac must pass
  # `--platform linux/amd64`, or this must say ARM64 and the image be built for
  # it. Leaving the field out means the mismatch is silent in the configuration
  # and only visible in a task that will not stay up.
  runtime_platform {
    cpu_architecture        = var.cpu_architecture
    operating_system_family = "LINUX"
  }

  container_definitions = jsonencode([{
    name      = "api"
    image     = "${aws_ecr_repository.this.repository_url}:${var.image_tag}"
    essential = true

    portMappings = [{
      containerPort = var.container_port
      protocol      = "tcp"
    }]

    # Plain configuration. Anything here is visible to anyone who can call
    # DescribeTaskDefinition, so nothing secret goes in this list.
    environment = [
      # Deliberately NOT "local". application.properties defaults to the `local`
      # profile, whose application-local.properties is GITIGNORED - so it is
      # present in an image built on a developer laptop and absent from one built
      # in CI. That difference is invisible until the two images behave
      # differently. `aws` has no properties file at all; everything below is
      # explicit.
      { name = "SPRING_PROFILES_ACTIVE", value = "aws" },
      {
        name = "SPRING_DATASOURCE_URL"
        # Spring Boot's relaxed binding maps SPRING_DATASOURCE_URL onto
        # spring.datasource.url, so no properties file is needed for any of this.
        #
        # connectionTimeZone=LOCAL and preserveInstants=false are carried over
        # from the app's own configuration and are load-bearing: the entities use
        # LocalDateTime, and any zone conversion is silent data corruption.
        value = "jdbc:mysql://${var.db_address}:${var.db_port}/${var.db_name}?useSSL=true&requireSSL=false&connectionTimeZone=LOCAL&preserveInstants=false"
      },
      { name = "SERVER_PORT", value = tostring(var.container_port) },

      # ⚠️ MUST NOT BE EMPTY, and the first apply proved it the hard way.
      #
      # PizzaProperties declares `Cors(@NotEmpty List<String> allowedOrigins)`, so
      # an empty value binds to an empty list and fails validation at startup. The
      # container exited 1, ECS started another, and the target group flipped
      # between `initial` and `draining` forever. The service events said nothing
      # useful; the reason was only in CloudWatch:
      #
      #     Property: pizza.cors.allowedOrigins
      #     Value: "[]"
      #     Reason: must not be empty
      #
      # Defaulting to the load balancer's own hostname is both non-empty and
      # correct: that IS the origin this API is served from. Referencing
      # aws_lb.this here is not a cycle - the load balancer does not depend on the
      # task definition.
      {
        name  = "PIZZA_CORS_ALLOWED_ORIGINS"
        value = var.cors_allowed_origins != "" ? var.cors_allowed_origins : "http://${aws_lb.this.dns_name}"
      },
    ]

    # Resolved by the ECS agent BEFORE the container starts, using the execution
    # role, and injected as environment variables. The values never appear in the
    # task definition, in state, or in the console.
    #
    # The `:key::` suffix selects one field out of a JSON secret. RDS stores its
    # managed password as {"username":…,"password":…}, so without the suffix the
    # application would receive the whole JSON document as its password.
    # The two trailing colons are version-stage and version-id, left empty to mean
    # "current" - they are required even when empty.
    secrets = [
      {
        name      = "SPRING_DATASOURCE_USERNAME"
        valueFrom = "${var.db_secret_arn}:username::"
      },
      {
        name      = "SPRING_DATASOURCE_PASSWORD"
        valueFrom = "${var.db_secret_arn}:password::"
      },
      {
        name      = "PIZZA_JWT_SECRET"
        valueFrom = aws_secretsmanager_secret.jwt.arn
      },
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.this.name
        "awslogs-region"        = data.aws_region.current.region
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])

  tags = var.tags
}

resource "aws_ecs_service" "this" {
  name            = var.name_prefix
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [var.app_security_group_id]

    # false, because the tasks are in private subnets and reach the internet
    # through the NAT gateway. Setting this true in a private subnet does not
    # help - there is no internet gateway route - and it is a common wrong fix
    # for the "cannot pull image" symptom, whose real cause is missing routing.
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.this.arn
    container_name   = "api"
    container_port   = var.container_port
  }

  # How long the ALB is allowed to report a new task unhealthy before ECS gives
  # up on it. A Spring Boot app with Liquibase migrations needs well over the
  # 0-second default on a cold start, and without this the service kills each
  # task just before it finishes booting - forever.
  health_check_grace_period_seconds = var.health_check_grace_period

  # ⚠️ Without this, apply races the IAM role.
  #
  # ECS validates that it can assume the execution role at service-creation time,
  # and IAM is eventually consistent - a role created moments earlier may not be
  # visible yet. Terraform sees no dependency here because the service references
  # the role only indirectly, through the task definition.
  depends_on = [
    aws_lb_listener.http,
    aws_iam_role_policy_attachment.execution_managed,
    aws_iam_role_policy.execution_secrets,
  ]

  tags = var.tags
}
