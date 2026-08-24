# The pizza API on AWS: network, database, and the service itself.
#
# This is the stack lessons 12, 13 and 14 of the /terraform track are written
# against. It was applied to a real account, verified through the load balancer,
# and destroyed. See projects/terraform_tutorial/progress_report.md.
#
#   terraform init
#   terraform plan
#   terraform apply
#   terraform destroy        # <- do not skip this, it costs ~$0.13/hour
#
# ⚠️ Costs money while it is up. Rough hourly, us-west-2:
#     NAT gateway   $0.045     ALB          $0.023
#     RDS t4g.micro $0.016     Fargate      $0.020   (0.5 vCPU / 1 GB)
#   About $0.13/hour, or ~$92/month if left running. There is no free tier for
#   any of it except the RDS instance in a new account's first year.

locals {
  # Every resource carries these, so `destroy` is provably complete and nothing
  # collides with the unrelated ECS clusters already in this account.
  tags = merge(var.tags, {
    Project   = "terraform-tutorial"
    ManagedBy = "terraform"
  })
}

module "network" {
  source = "./modules/network"

  name_prefix = var.name_prefix
  vpc_cidr    = var.vpc_cidr
  tags        = local.tags
}

# ⚠️ THE APPLICATION SECURITY GROUP LIVES HERE, NOT IN A MODULE.
#
# The database module needs it, to write "allow MySQL from this group". The
# service module needs it, to attach to the tasks - and the service module also
# needs the database's endpoint for the JDBC URL.
#
# Put it in either module and those two modules reference each other, and
# Terraform stops with "Cycle: module.database..., module.service...". Hoisting
# the shared value up to the common caller is the standard fix, and it is worth
# recognising the shape: a cycle between modules is nearly always a value that
# belongs to whoever calls them both.
resource "aws_security_group" "app" {
  name        = "${var.name_prefix}-app"
  description = "The pizza API tasks"
  vpc_id      = module.network.vpc_id
  tags        = merge(local.tags, { Name = "${var.name_prefix}-app" })
}

# Only the load balancer may reach the application port. The tasks are in private
# subnets, so this is defence in depth rather than the only control - but it is
# the one that still holds if the routing is later changed.
resource "aws_vpc_security_group_ingress_rule" "app_from_alb" {
  security_group_id            = aws_security_group.app.id
  description                  = "Application port, from the load balancer only"
  from_port                    = var.container_port
  to_port                      = var.container_port
  ip_protocol                  = "tcp"
  referenced_security_group_id = module.service.alb_security_group_id
}

# Outbound to anywhere. The task must reach ECR for its image, Secrets Manager
# for its configuration, CloudWatch for its logs, and RDS - all through the NAT
# gateway. Narrowing this to specific destinations means maintaining AWS's
# published IP ranges, which is why almost nobody does.
#
# `-1` means every protocol, and AWS requires the port range to be omitted when
# it is - passing from_port/to_port alongside it is rejected.
resource "aws_vpc_security_group_egress_rule" "app_all" {
  security_group_id = aws_security_group.app.id
  description       = "All outbound"
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"
}

module "database" {
  source = "./modules/database"

  name_prefix           = var.name_prefix
  vpc_id                = module.network.vpc_id
  private_subnet_ids    = module.network.private_subnet_ids
  app_security_group_id = aws_security_group.app.id
  tags                  = local.tags
}

module "service" {
  source = "./modules/service"

  name_prefix           = var.name_prefix
  vpc_id                = module.network.vpc_id
  public_subnet_ids     = module.network.public_subnet_ids
  private_subnet_ids    = module.network.private_subnet_ids
  app_security_group_id = aws_security_group.app.id

  db_address    = module.database.address
  db_port       = module.database.port
  db_name       = module.database.database_name
  db_secret_arn = module.database.master_user_secret_arn

  image_tag        = var.image_tag
  container_port   = var.container_port
  desired_count    = var.desired_count
  cpu_architecture = var.cpu_architecture

  tags = local.tags
}
