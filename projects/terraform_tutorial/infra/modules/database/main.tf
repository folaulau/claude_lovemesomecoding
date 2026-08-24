# RDS MySQL for the pizza API.
#
# Quoted by lesson 12 of the /terraform track on lovemesomecoding.com.
#
# The interesting part of this module is not the database - it is that the
# password is never in the Terraform state file. See manage_master_user_password
# below; it is the single most useful thing in here.

# A DB subnet group tells RDS which subnets it may place the instance in. It
# requires at least two, in different AZs, EVEN FOR A SINGLE-AZ INSTANCE - AWS
# wants somewhere to fail over to before it will let you opt out of failing over.
resource "aws_db_subnet_group" "this" {
  name       = "${var.name_prefix}-db"
  subnet_ids = var.private_subnet_ids
  tags       = merge(var.tags, { Name = "${var.name_prefix}-db" })
}

# ⚠️ NO CIDR BLOCK IN THIS RULE.
#
# `source_security_group_id` allows traffic from anything wearing that security
# group, wherever it happens to be and whatever address it has. Fargate tasks get
# a new private IP every time they start, so a CIDR-based rule here would either
# be wrong or so wide it allowed the whole VPC.
#
# This is the single most useful habit in AWS networking: security groups
# referencing security groups, not addresses.
resource "aws_security_group" "db" {
  name        = "${var.name_prefix}-db"
  description = "MySQL access for the pizza API tasks"
  vpc_id      = var.vpc_id
  tags        = merge(var.tags, { Name = "${var.name_prefix}-db" })
}

resource "aws_vpc_security_group_ingress_rule" "db_from_app" {
  security_group_id = aws_security_group.db.id
  description       = "MySQL from the ECS tasks"

  from_port                    = 3306
  to_port                      = 3306
  ip_protocol                  = "tcp"
  referenced_security_group_id = var.app_security_group_id
}

# Note there is deliberately NO egress rule on the database security group.
#
# A security group with no egress rules allows nothing out, and a database has no
# business opening outbound connections. Terraform's older `aws_security_group`
# with inline blocks would have silently kept AWS's default allow-all egress;
# these separate rule resources make the absence explicit and reviewable.

resource "aws_db_instance" "this" {
  identifier = "${var.name_prefix}-mysql"

  engine         = "mysql"
  engine_version = var.engine_version
  instance_class = var.instance_class

  # gp3 rather than the older gp2. Same price per GB in every region, better
  # baseline throughput, and 20 GB is the minimum RDS accepts for MySQL.
  allocated_storage = 20
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = var.database_name
  username = var.master_username

  # ⚠️ THE POINT OF THIS MODULE.
  #
  # With `password = var.db_password`, the password is in the state file in
  # PLAINTEXT - forever, in every historical version, in the S3 bucket, readable
  # by anyone who can read state. Marking the variable `sensitive` only hides it
  # from console output; it changes nothing about what is written to disk.
  #
  # This instead has RDS generate the password, store it in Secrets Manager, and
  # own its rotation. Terraform never learns it. The ECS task definition reads it
  # straight from the secret ARN exported below, so it never passes through here
  # at all.
  manage_master_user_password = true

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.db.id]

  # No public address. The only route to this database is from inside the VPC,
  # which is what the security group above then narrows to just the tasks.
  publicly_accessible = false

  # Single AZ, deliberately: multi_az doubles the cost to buy a failover this
  # demo does not need. Production says true.
  multi_az = false

  # ---- the three arguments that make `terraform destroy` actually work -------
  #
  # Defaults here are tuned for a real database, and every one of them fights a
  # teardown. On a demo stack that is meant to be destroyed, they cost money and
  # block the destroy with errors that arrive several minutes in.
  skip_final_snapshot     = true  # default false: destroy fails asking for a snapshot name
  deletion_protection     = false # production says true, and then destroy refuses outright
  backup_retention_period = 0     # default 1 day: automated backups bill after the instance is gone
  apply_immediately       = true

  tags = merge(var.tags, { Name = "${var.name_prefix}-mysql" })
}
