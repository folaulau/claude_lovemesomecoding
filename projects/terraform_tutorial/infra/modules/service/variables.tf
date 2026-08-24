variable "name_prefix" {
  type        = string
  description = "Prefix for every resource name."
}

variable "vpc_id" {
  type        = string
  description = "VPC the load balancer and tasks live in."
}

variable "public_subnet_ids" {
  type        = list(string)
  description = "Public subnets for the ALB. Must span at least two AZs."

  validation {
    condition     = length(var.public_subnet_ids) >= 2
    error_message = "An application load balancer requires subnets in at least two availability zones."
  }
}

variable "private_subnet_ids" {
  type        = list(string)
  description = "Private subnets for the Fargate tasks."
}

variable "app_security_group_id" {
  type        = string
  description = <<-EOT
    Security group worn by the tasks.

    Created by the ROOT module, not here, and that is deliberate. The database
    module needs it to write its ingress rule, and this module needs the database
    endpoint for the JDBC URL - so if either module owned it, the two modules
    would depend on each other and Terraform would refuse with a cycle error.
    Hoisting the shared value to the caller is the standard way out.
  EOT
}

variable "db_address" {
  type        = string
  description = "RDS hostname."
}

variable "db_port" {
  type        = number
  description = "RDS port."
}

variable "db_name" {
  type        = string
  description = "Schema name."
}

variable "db_secret_arn" {
  type        = string
  description = "ARN of the RDS-managed master password secret. Read by the ECS agent, never by Terraform."
}

variable "image_tag" {
  type        = string
  default     = "latest"
  description = <<-EOT
    Image tag to run.

    The pipeline passes the git SHA. `latest` is the default only so the first
    apply has something to reference before any image exists; deploying it means
    you cannot answer "what is actually running?" See lesson 14.
  EOT
}

variable "container_port" {
  type        = number
  default     = 8085
  description = "Port the app binds. Matches server.port in application.properties."
}

variable "health_check_path" {
  type        = string
  default     = "/actuator/health/alb"
  description = <<-EOT
    ⚠️ A health GROUP, not the aggregate endpoint.

    /actuator/health returns 503 whenever any optional dependency is down, which
    on this app means whenever Artemis is unreachable - i.e. always, on ECS. The
    `alb` group contains only `ping`. See the demo app's application.properties.
  EOT
}

variable "task_cpu" {
  type        = string
  default     = "512"
  description = "Fargate CPU units. 512 = 0.5 vCPU, which permits 1024-4096 MB of memory."
}

variable "task_memory" {
  type        = string
  default     = "1024"
  description = "Fargate memory in MB. Must be a valid pairing with task_cpu."
}

variable "desired_count" {
  type        = number
  default     = 1
  description = "Number of tasks. One has no redundancy; it is what a demo needs."
}

variable "health_check_grace_period" {
  type        = number
  default     = 180
  description = "Seconds before ECS starts honouring the ALB health check. Boot + Liquibase needs it."
}

variable "log_retention_days" {
  type        = number
  default     = 7
  description = "CloudWatch retention. Unset means keep forever, and bill forever."
}

variable "cors_allowed_origins" {
  type        = string
  default     = ""
  description = "Comma-separated origins for pizza.cors.allowed-origins. Empty when nothing browser-facing calls it cross-origin."
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags applied to every resource in this module."
}

variable "cpu_architecture" {
  type        = string
  default     = "ARM64"
  description = <<-EOT
    X86_64 or ARM64, and it MUST match what the image was built for.

    ARM64 runs on Graviton and is roughly 20% cheaper per Fargate task, and it is
    a native build on an Apple Silicon laptop. The catch is CI: a standard
    ubuntu-latest GitHub runner is x86, so it would have to cross-build under
    QEMU - which for a Maven build is slow enough to notice.

    X86_64 is the default because it is what a stock pipeline produces. A Mac
    must then build with `docker build --platform linux/amd64`, or the task dies
    with `exec format error`.
  EOT

  validation {
    condition     = contains(["X86_64", "ARM64"], var.cpu_architecture)
    error_message = "cpu_architecture must be X86_64 or ARM64."
  }
}
