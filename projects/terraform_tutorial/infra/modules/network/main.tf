# The network the pizza API runs in: one VPC, public subnets for the load
# balancer, private subnets for the tasks and the database.
#
# Quoted by lesson 12 of the /terraform track on lovemesomecoding.com.
#
# The shape is the standard one, and it is worth saying why rather than just
# drawing it:
#
#   internet
#      |
#   [internet gateway]
#      |
#   public subnets   ..... the load balancer lives here, and the NAT gateway
#      |
#   private subnets  ..... the ECS tasks and RDS live here
#
# Nothing in a private subnet has a route from the internet, so nothing on the
# internet can open a connection to it. The tasks still need OUTBOUND access to
# pull their image from ECR and write logs, which is what the NAT gateway is for.

# Two availability zones, chosen at plan time rather than hard-coded.
#
# `us-west-2a` in your account and `us-west-2a` in mine are not necessarily the
# same physical datacentre - AWS shuffles the letter-to-AZ mapping per account,
# which is why hard-coding them makes a configuration that is not portable. It
# also breaks outright in a region that has retired an AZ letter.
#
# `state = "available"` filters out AZs that exist but are not currently taking
# new resources.
data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  # Take exactly two. An ALB REQUIRES subnets in at least two AZs and refuses to
  # create with one - the error names "at least two subnets" without mentioning
  # availability zones, which is a confusing way to learn this.
  azs = slice(data.aws_availability_zones.available.names, 0, 2)

  # 10.20.0.0/16 gives 65,536 addresses, carved into four /24s of 256 each.
  # Deliberately NOT 172.31.0.0/16: that is what the account's DEFAULT VPC uses,
  # and overlapping CIDRs make the two impossible to peer later. Picking a range
  # nothing else uses costs nothing today and removes a whole class of problem.
  public_cidrs  = ["10.20.0.0/24", "10.20.1.0/24"]
  private_cidrs = ["10.20.10.0/24", "10.20.11.0/24"]
}

resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr

  # Both are required for RDS to be reachable by hostname, and both default to
  # false on a VPC you create yourself - unlike the default VPC, where they are
  # already on. RDS hands out a DNS name; without enable_dns_hostnames there is
  # no name to resolve and the app fails with an unknown-host error that reads
  # like a typo in the connection string.
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(var.tags, { Name = var.name_prefix })
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
  tags   = merge(var.tags, { Name = "${var.name_prefix}-igw" })
}

# ------------------------------------------------------------------ subnets
#
# count, not for_each, and this is the case where count is right: the subnets
# are an ordered pair with no meaningful identity of their own, indexed by AZ.
# See lesson 9 for the general rule - for_each is the better default, because
# removing the middle element of a count list renumbers everything after it and
# Terraform destroys and recreates the lot.
resource "aws_subnet" "public" {
  count = length(local.azs)

  vpc_id            = aws_vpc.this.id
  cidr_block        = local.public_cidrs[count.index]
  availability_zone = local.azs[count.index]

  # This is what makes the subnet "public" in the sense the ALB cares about.
  # It is not what makes it routable - the route table below does that.
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.name_prefix}-public-${local.azs[count.index]}"
    Tier = "public"
  })
}

resource "aws_subnet" "private" {
  count = length(local.azs)

  vpc_id            = aws_vpc.this.id
  cidr_block        = local.private_cidrs[count.index]
  availability_zone = local.azs[count.index]

  tags = merge(var.tags, {
    Name = "${var.name_prefix}-private-${local.azs[count.index]}"
    Tier = "private"
  })
}

# ------------------------------------------------------------------ NAT
#
# ⚠️ THIS IS THE LINE ITEM ON YOUR BILL.
#
# A NAT gateway is roughly $0.045/hour - about $32/month - plus $0.045 per GB
# processed, and it bills whether or not anything sends a byte through it. It is
# the single most common surprise in an ECS bill, and it is why a "free tier"
# ECS tutorial usually is not.
#
# ONE gateway, not one per AZ. Two would be the highly-available answer, because
# a NAT gateway lives in a single AZ and takes that AZ's outbound traffic with it
# when it fails. This doubles the cost to buy resilience a demo does not need, so
# it is a deliberate trade and not an oversight. Production in two AZs should
# have two.
#
# The alternatives, honestly:
#   - Public subnets + assign_public_ip = true. Free, and the tasks then have
#     inbound-capable addresses. Fine for a demo, wrong as a default.
#   - VPC interface endpoints for ECR/S3/Logs. Better at scale, but it takes FIVE
#     of them to run Fargate privately and they are ~$0.01/hr EACH - so about
#     $0.05/hr, which is MORE than this NAT gateway, until data volume is high
#     enough for the per-GB charge to dominate.
resource "aws_eip" "nat" {
  domain = "vpc"
  tags   = merge(var.tags, { Name = "${var.name_prefix}-nat" })

  # The EIP is allocated from a pool the internet gateway must already exist to
  # draw from. Terraform cannot see that dependency in the arguments, because
  # neither resource references the other - so it has to be stated.
  depends_on = [aws_internet_gateway.this]
}

resource "aws_nat_gateway" "this" {
  allocation_id = aws_eip.nat.id

  # ⚠️ In a PUBLIC subnet. A NAT gateway's whole job is to have a route to the
  # internet gateway; putting it in the private subnet it serves creates a
  # routing loop that Terraform will happily build for you.
  subnet_id = aws_subnet.public[0].id

  tags       = merge(var.tags, { Name = "${var.name_prefix}-nat" })
  depends_on = [aws_internet_gateway.this]
}

# ------------------------------------------------------------ route tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }

  tags = merge(var.tags, { Name = "${var.name_prefix}-public" })
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.this.id
  }

  tags = merge(var.tags, { Name = "${var.name_prefix}-private" })
}

# A route table does nothing until a subnet is associated with it. This is the
# step people skip, and the symptom is a task that starts, cannot pull its image,
# and times out several minutes later with no mention of routing.
resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(aws_subnet.private)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}
