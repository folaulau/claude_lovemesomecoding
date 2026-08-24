output "app_url" {
  description = "Open this. It is the load balancer's public hostname."
  value       = module.service.app_url
}

output "ecr_repository_url" {
  description = "docker push here."
  value       = module.service.ecr_repository_url
}

output "cluster_name" { value = module.service.cluster_name }
output "service_name" { value = module.service.service_name }
output "log_group_name" { value = module.service.log_group_name }

output "db_endpoint" {
  description = "RDS endpoint. Not reachable from outside the VPC."
  value       = module.database.endpoint
}

# Note what is NOT here: the database password. It is never an output because it
# is never a value Terraform holds - RDS generated it into Secrets Manager and
# the ECS agent reads it directly. Read it, if you need it, with:
#   aws secretsmanager get-secret-value --secret-id <arn> --query SecretString
output "db_secret_arn" {
  description = "ARN of the RDS-managed master password secret."
  value       = module.database.master_user_secret_arn
}
