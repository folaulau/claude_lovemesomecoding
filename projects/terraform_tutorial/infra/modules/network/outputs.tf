# Outputs are this module's public API. Everything the service and database
# modules need to attach to the network comes through here - which is what makes
# the module replaceable without editing its callers.

output "vpc_id" {
  description = "Id of the VPC."
  value       = aws_vpc.this.id
}

output "vpc_cidr" {
  description = "CIDR of the VPC, for security group rules that allow VPC-internal traffic."
  value       = aws_vpc.this.cidr_block
}

output "public_subnet_ids" {
  description = "Public subnets, for the load balancer."
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnets, for the ECS tasks and RDS."
  value       = aws_subnet.private[*].id
}

output "availability_zones" {
  description = "The AZs actually chosen, which are resolved at plan time."
  value       = local.azs
}
