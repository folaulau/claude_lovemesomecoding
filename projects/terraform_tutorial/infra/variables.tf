variable "name_prefix" {
  type        = string
  default     = "pizza-tf"
  description = <<-EOT
    Prefix on every resource name.

    Load-bearing for teardown: this account already holds three unrelated ECS
    clusters (learnmymath-api, development, pocsoft), so "delete the ECS cluster"
    is not a safe instruction. Everything this stack creates is `pizza-tf-*` and
    tagged Project=terraform-tutorial.
  EOT

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,20}$", var.name_prefix))
    error_message = "name_prefix must be lowercase letters, digits and hyphens, 3-21 chars, starting with a letter."
  }
}

variable "region" {
  type        = string
  default     = "us-west-2"
  description = "Region to deploy into."
}

variable "vpc_cidr" {
  type        = string
  default     = "10.20.0.0/16"
  description = "Must not overlap the account's default VPC (172.31.0.0/16)."
}

variable "image_tag" {
  type        = string
  default     = "latest"
  description = "Image tag to run. The pipeline passes a git SHA."
}

variable "container_port" {
  type        = number
  default     = 8085
  description = "Port the app binds. Matches server.port."
}

variable "desired_count" {
  type        = number
  default     = 1
  description = "Number of tasks to run."
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Extra tags, merged with the Project/ManagedBy pair every resource gets."
}

variable "cpu_architecture" {
  type        = string
  default     = "ARM64"
  description = <<-EOT
    Must match the architecture the image was built for.

    ARM64 is the default here for three reasons, in order of how much they
    mattered: Fargate on Graviton is ~20% cheaper, this repository is authored on
    an Apple Silicon Mac so the image builds NATIVELY, and GitHub now offers free
    arm64 runners (`ubuntu-24.04-arm`) so CI is native too.

    ⚠️ The x86 alternative was tried first and is genuinely painful from a Mac.
    `docker buildx build --platform linux/amd64` on this Dockerfile fails inside
    the Maven wrapper:

        tar: apache-maven-3.9.16/lib/asm-9.9.1.jar: Cannot open: Function not implemented
        tar: Exiting with failure status due to previous errors

    That is QEMU's amd64 emulation missing a syscall that GNU tar uses, not
    anything wrong with the build. Going x86 from an ARM machine therefore means
    either a `--platform=$BUILDPLATFORM` build stage or building the jar on the
    host — both fine, both extra moving parts this does not need.

    Set X86_64 if your image is x86, and remember it must be BOTH here and in the
    `docker build --platform` that produced the image. A mismatch is not caught at
    deploy time; the task starts and dies with `exec format error`.
  EOT

  validation {
    condition     = contains(["X86_64", "ARM64"], var.cpu_architecture)
    error_message = "cpu_architecture must be X86_64 or ARM64."
  }
}
