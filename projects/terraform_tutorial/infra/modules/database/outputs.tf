output "endpoint" {
  description = "host:port for the instance."
  value       = aws_db_instance.this.endpoint
}

output "address" {
  description = "Hostname only, for building a JDBC URL."
  value       = aws_db_instance.this.address
}

output "port" {
  description = "Port the instance listens on."
  value       = aws_db_instance.this.port
}

output "database_name" {
  description = "The initial schema name."
  value       = aws_db_instance.this.db_name
}

output "master_username" {
  description = "The master username."
  value       = aws_db_instance.this.username
}

# The ARN of the Secrets Manager secret RDS created and owns.
#
# This is how the password reaches the application without passing through
# Terraform. The secret's value is a JSON document {"username":…,"password":…},
# so the ECS task definition selects the field it wants with the
# `arn:json-key::` suffix - see the service module.
output "master_user_secret_arn" {
  description = "ARN of the RDS-managed master password secret."
  value       = aws_db_instance.this.master_user_secret[0].secret_arn
}

output "security_group_id" {
  description = "The database security group, for anything else that needs to reach it."
  value       = aws_security_group.db.id
}
