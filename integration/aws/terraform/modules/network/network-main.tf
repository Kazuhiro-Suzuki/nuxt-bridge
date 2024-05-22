resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  instance_tenancy     = "default"
  enable_dns_support   = "true"
  enable_dns_hostnames = "true"

  tags = {
    Name = "${var.name}-vpc"
  }
}

resource "aws_default_security_group" "default" {
  vpc_id = aws_vpc.this.id
}

resource "aws_flow_log" "this" {
  iam_role_arn    = aws_iam_role.vpc-flow-log-role.arn
  log_destination = aws_cloudwatch_log_group.vpc-flow-log.arn
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.this.id
}

resource "aws_cloudwatch_log_group" "vpc-flow-log" {
  name              = "/vpc/flow-log/${var.name}"
  retention_in_days = var.retention_in_days
}

resource "aws_iam_role" "vpc-flow-log-role" {
  name = "${var.name}-vpc-flow-log-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "vpc-flow-logs.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "vpc-flow-log-role-policy" {
  name = "${var.name}-vpc-flow-log-role-policy"
  role = aws_iam_role.vpc-flow-log-role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "${var.name}-igw"
  }
}

resource "aws_eip" "nat_gateway" {
  vpc = true

  tags = {
    Name = "${var.name}-ngw-eip"
  }
}

resource "aws_nat_gateway" "this" {
  allocation_id = aws_eip.nat_gateway.id
  //  subnet_id     = aws_subnet.public_a.id
  subnet_id = aws_subnet.public-subnet[0].id

  tags = {
    Name = "${var.name}-ngw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }

  tags = {
    Name = "${var.name}-public-rt"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.this.id
  }

  tags = {
    Name = "${var.name}-private-rt"
  }
}

resource "aws_subnet" "public-subnet" {
  count = length(var.public_subnets)

  vpc_id                  = aws_vpc.this.id
  availability_zone       = element(keys(var.public_subnets), count.index)
  cidr_block              = element(values(var.public_subnets), count.index)
  map_public_ip_on_launch = true

  tags = {
    Name = "${element(keys(var.public_subnets), count.index)}-public-subnet"
  }
}

resource "aws_subnet" "private-subnet" {
  count = length(var.private_subnets)

  vpc_id                  = aws_vpc.this.id
  availability_zone       = element(keys(var.private_subnets), count.index)
  cidr_block              = element(values(var.private_subnets), count.index)
  map_public_ip_on_launch = false

  tags = {
    Name = "${element(keys(var.private_subnets), count.index)}-private-subnet"
  }
}

resource "aws_route_table_association" "public-subnet" {
  count = length(var.public_subnets)

  subnet_id      = element(aws_subnet.public-subnet.*.id, count.index)
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private-subnet" {
  count = length(var.private_subnets)

  subnet_id      = element(aws_subnet.private-subnet.*.id, count.index)
  route_table_id = aws_route_table.private.id
}

resource "aws_security_group" "lb" {
  name   = "${var.name}-lb-sg"
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "${var.name}-lb-sg"
  }


  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    prefix_list_ids = ["pl-58a04531"] # CloudFrontのIPを管理するマネージドプレフィックスリストのみ許可する
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.allow_ips # Django管理画面へのアクセスは特定IPからのみ許可する
  }

  # アプリ経由のアクセスを許可する（アプリ側のURLを修正後にこの設定は削除すること）
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "for mobile"
  }
  # アプリ経由のアクセスを許可する（アプリ側のURLを修正後にこの設定は削除すること）

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ecs" {
  name   = "${var.name}-ecs-sg"
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "${var.name}-ecs-sg"
  }

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.lb.id]
  }

  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.lb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "bastion" {
  name   = "${var.name}-bastion-sg"
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "${var.name}-bastion-sg"
  }

  egress {
    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "db" {
  name   = "${var.name}-db-sg"
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "${var.name}-db-sg"
  }

  ingress {
    from_port       = var.db_port
    to_port         = var.db_port
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id, aws_security_group.bastion.id]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# bastion
data "aws_iam_policy_document" "assume-role-for-ec2-policy-document" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "systems-manager-role" {
  name               = "${var.name}-systems-manager-role"
  assume_role_policy = data.aws_iam_policy_document.assume-role-for-ec2-policy-document.json
}

data "aws_iam_policy" "systems-manager-policy" {
  arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "systems-manager-role-policy-attachment" {
  role       = aws_iam_role.systems-manager-role.name
  policy_arn = data.aws_iam_policy.systems-manager-policy.arn
}

resource "aws_iam_instance_profile" "systems-manager" {
  name = "${var.name}-instance-profile"
  role = aws_iam_role.systems-manager-role.name
}

data "template_cloudinit_config" "user_data" {
  gzip          = false
  base64_encode = false

  part {
    content_type = "text/x-shellscript"
    content      = <<EOF
    #!/bin/bash
    sudo yum update -y
    sudo yum install -y postgresql.x86_64
    EOF
  }
}

resource "aws_kms_key" "encrypt_key" {
  deletion_window_in_days = 10
}

resource "aws_kms_alias" "encrypt_key" {
  name          = "alias/${var.name}-kms-key-for-bastion-ebs-encrypt"
  target_key_id = aws_kms_key.encrypt_key.key_id
}

resource "aws_instance" "bastion" {
  ami                    = var.bastion_ami
  instance_type          = "t2.micro"
  key_name               = var.bastion_key_pair
  vpc_security_group_ids = [aws_security_group.bastion.id]
  subnet_id              = aws_subnet.private-subnet[0].id
  iam_instance_profile   = aws_iam_instance_profile.systems-manager.name
  user_data              = data.template_cloudinit_config.user_data.rendered
  //  associate_public_ip_address = "true"

  root_block_device {
    encrypted  = true
    kms_key_id = aws_kms_key.encrypt_key.arn
  }

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  tags = {
    Name = "${var.name}-bastion"
  }
}


####################
# VPC Endpoint
####################
resource "aws_security_group" "vpce" {
  name   = "${var.name}-vpce-sg"
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "${var.name}-ecs-sg"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.this.cidr_block]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.this.cidr_block]
  }
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.this.id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
}

resource "aws_vpc_endpoint_route_table_association" "private_s3" {
  count           = length(aws_subnet.private-subnet)
  vpc_endpoint_id = aws_vpc_endpoint.s3.id
  route_table_id  = aws_route_table.private.id
}

resource "aws_vpc_endpoint" "ecr_dkr" {
  vpc_id              = aws_vpc.this.id
  service_name        = "com.amazonaws.${var.region}.ecr.dkr"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.private-subnet[*].id
  security_group_ids  = [aws_security_group.vpce.id]
  private_dns_enabled = true
}

resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id              = aws_vpc.this.id
  service_name        = "com.amazonaws.${var.region}.ecr.api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.private-subnet[*].id
  security_group_ids  = [aws_security_group.vpce.id]
  private_dns_enabled = true
}

resource "aws_vpc_endpoint" "logs" {
  vpc_id              = aws_vpc.this.id
  service_name        = "com.amazonaws.${var.region}.logs"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.private-subnet[*].id
  security_group_ids  = [aws_security_group.vpce.id]
  private_dns_enabled = true
}
