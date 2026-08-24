output "alb_dns_name" {
  description = "Public hostname of the load balancer. This is the application's URL."
  value       = aws_lb.this.dns_name
}

output "app_url" {
  description = "Ready-to-open URL."
  value       = "http://${aws_lb.this.dns_name}"
}

output "ecr_repository_url" {
  description = "Where the pipeline pushes images."
  value       = aws_ecr_repository.this.repository_url
}

output "cluster_name" {
  description = "ECS cluster name, for `aws ecs update-service`."
  value       = aws_ecs_cluster.this.name
}

output "service_name" {
  description = "ECS service name, for forcing a new deployment."
  value       = aws_ecs_service.this.name
}

output "log_group_name" {
  description = "CloudWatch log group holding the application logs."
  value       = aws_cloudwatch_log_group.this.name
}

output "target_group_arn" {
  description = "Target group, for checking target health during a deploy."
  value       = aws_lb_target_group.this.arn
}

# Consumed by the ROOT module, to allow the application port from this group.
#
# The reverse rule - ALB egress to the tasks - is written inside this module,
# against var.app_security_group_id. The two rules therefore point at each other
# across the module boundary, which looks like it should be a cycle and is not:
# Terraform's graph is per-resource, and neither SECURITY GROUP depends on the
# other, only the RULES do. Writing them as inline `ingress`/`egress` blocks on
# the security groups instead WOULD deadlock, which is a good reason to prefer
# the separate rule resources.
output "alb_security_group_id" {
  description = "Security group of the load balancer."
  value       = aws_security_group.alb.id
}
