variable "name_prefix" {
  type        = string
  description = "Prefix for every resource name."
}

variable "vpc_id" {
  type        = string
  description = "VPC to create the security group in."
}

variable "private_subnet_ids" {
  type        = list(string)
  description = "Private subnets for the DB subnet group. RDS requires at least two AZs."

  validation {
    condition     = length(var.private_subnet_ids) >= 2
    error_message = "RDS needs subnets in at least two availability zones, even for a single-AZ instance."
  }
}

variable "app_security_group_id" {
  type        = string
  description = "Security group of the ECS tasks. Only this group may reach MySQL."
}

variable "engine_version" {
  type        = string
  default     = "8.4"
  description = "MySQL major version. 8.4 matches the compose stack the app is developed against."
}

variable "instance_class" {
  type        = string
  default     = "db.t4g.micro"
  description = "db.t4g.micro is Graviton, and cheaper than the equivalent t3."
}

variable "database_name" {
  type        = string
  default     = "pizza"
  description = "Initial schema. Liquibase creates the tables; it cannot create the schema."
}

variable "master_username" {
  type        = string
  default     = "pizza"
  description = "Master user. NOT 'admin' or 'root' - both are reserved by RDS and rejected."
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags applied to every resource in this module."
}
