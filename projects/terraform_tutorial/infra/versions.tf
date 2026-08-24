# Version constraints and the provider configuration.
#
# Quoted by lesson 4 of the /terraform track.

terraform {
  # ">= 1.10" and not "= 1.15.9". Pinning Terraform itself to one patch means
  # every colleague and every CI runner must match exactly, which is friction
  # with no safety benefit - the language is stable across minors.
  #
  # 1.10 specifically, because that is the release that added native S3 state
  # locking (`use_lockfile`), which backend.tf uses. An older Terraform reads
  # that file, does not recognise the argument, and proceeds with NO LOCKING at
  # all rather than failing - so the floor here is what makes the lock real.
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source = "hashicorp/aws"

      # ⚠️ `~> 6.0` means ">= 6.0, < 7.0" - the rightmost component may move.
      # Providers ship breaking changes in majors, so allowing 7.x would let a
      # routine `terraform init -upgrade` rewrite half this configuration's
      # meaning. The exact version in use is pinned by .terraform.lock.hcl, which
      # is committed; this constraint governs what the lock file is allowed to
      # move to.
      version = "~> 6.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "aws" {
  region = var.region

  # Applied to every resource this provider creates, on top of whatever tags the
  # resource sets. It is the backstop that makes the teardown query reliable:
  # even a resource where someone forgot `tags = local.tags` still carries this.
  default_tags {
    tags = {
      Project   = "terraform-tutorial"
      ManagedBy = "terraform"
    }
  }
}
