variable "name_prefix" {
  description = "Prefix for every resource name, so a destroy is provably complete."
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC. Must not overlap the default VPC's 172.31.0.0/16."
  type        = string
  default     = "10.20.0.0/16"

  # Caught at PLAN time, before anything is created. Without it, a /24 here would
  # create a VPC with no room for the four /24 subnets below it and fail halfway
  # through the apply - leaving a VPC behind that the next run has to reconcile.
  validation {
    condition     = can(cidrnetmask(var.vpc_cidr)) && tonumber(split("/", var.vpc_cidr)[1]) <= 20
    error_message = "vpc_cidr must be valid CIDR and /20 or larger to fit the subnets."
  }
}

variable "tags" {
  description = "Tags applied to every resource in this module."
  type        = map(string)
  default     = {}
}
