#----------------------------------------
# 情報取得
#----------------------------------------

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  region     = data.aws_region.current.name
}


locals {
  cluster_name        = "${var.name}-cls"
  monitoring_role_arn = var.create_monitoring_role ? aws_iam_role.enhanced_monitoring[0].arn : var.monitoring_role_arn
}

# Ref. https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces
data "aws_partition" "current" {}

resource "aws_kms_key" "encrypt_key" {
  deletion_window_in_days = 10
}

resource "aws_kms_alias" "encrypt_key" {
  name          = "alias/${var.name}-kms-key-for-rds-encrypt"
  target_key_id = aws_kms_key.encrypt_key.key_id
}


resource "aws_db_subnet_group" "this" {
  name       = "${var.name}-subnet-group"
  subnet_ids = var.private_subnets
  tags = {
    Name = "${var.name}-subnet-group"
  }
}

resource "aws_rds_cluster_parameter_group" "postgresql" {
  name   = "${local.cluster_name}-parameter-group"
  family = "aurora-postgresql11"
  lifecycle {
    create_before_destroy = true
  }
  parameter {
    name  = "timezone"
    value = "Asia/Tokyo"
  }
}

resource "aws_rds_cluster_parameter_group" "postgresql12" {
  name   = "${local.cluster_name}-parameter-group12"
  family = "aurora-postgresql12"
  lifecycle {
    create_before_destroy = true
  }
  parameter {
    name  = "timezone"
    value = "Asia/Tokyo"
  }
}

resource "aws_db_parameter_group" "postgresql" {
  name   = "${local.cluster_name}-parameter-group"
  family = "aurora-postgresql11"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_db_parameter_group" "postgresql12" {
  name   = "${local.cluster_name}-dbparameter-group12"
  family = "aurora-postgresql12"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_rds_cluster" "postgresql" {
  cluster_identifier   = local.cluster_name
  engine               = "aurora-postgresql"
  engine_version       = var.aurora_engine_version
  availability_zones   = var.availability_zones
  db_subnet_group_name = "${var.name}-subnet-group"
  #db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.postgresql.name
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.postgresql12.name
  deletion_protection             = true
  database_name                   = var.db_master_name
  master_username                 = var.db_master_user
  master_password                 = var.db_master_password

  storage_encrypted               = true
  kms_key_id                      = aws_kms_key.encrypt_key.arn
  backup_retention_period         = 30
  final_snapshot_identifier       = "final-rds-${var.name}"
  enabled_cloudwatch_logs_exports = ["postgresql"]

  vpc_security_group_ids      = [var.security_group.id]
  allow_major_version_upgrade = true
  apply_immediately           = true
}

resource "aws_rds_cluster_instance" "postgresql_instance" {
  count              = 1
  identifier         = "${local.cluster_name}-instance-${count.index}"
  cluster_identifier = aws_rds_cluster.postgresql.id
  instance_class     = "db.t3.medium"
  engine             = aws_rds_cluster.postgresql.engine
  #engine_version                  = aws_rds_cluster.postgresql.engine_version
  db_subnet_group_name = "${var.name}-subnet-group"
  #db_parameter_group_name         = aws_db_parameter_group.postgresql.name
  db_parameter_group_name = aws_db_parameter_group.postgresql12.name
  #db_parameter_group_name         = "default.aurora-postgresql11"
  performance_insights_enabled    = true
  performance_insights_kms_key_id = aws_kms_key.encrypt_key.arn
  monitoring_interval             = var.monitoring_interval
  monitoring_role_arn             = var.monitoring_interval > 0 ? local.monitoring_role_arn : null
  apply_immediately               = true
  depends_on = [
    aws_rds_cluster.postgresql
  ]
}

################################################################################
# Enhanced monitoring
################################################################################

data "aws_iam_policy_document" "enhanced_monitoring" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type        = "Service"
      identifiers = ["monitoring.rds.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "enhanced_monitoring" {
  count = var.create_monitoring_role ? 1 : 0

  name               = var.monitoring_role_name
  assume_role_policy = data.aws_iam_policy_document.enhanced_monitoring.json

  tags = {
    "Name" = format("%s", var.monitoring_role_name)
  }
}

resource "aws_iam_role_policy_attachment" "enhanced_monitoring" {
  count = var.create_monitoring_role ? 1 : 0

  role       = aws_iam_role.enhanced_monitoring[0].name
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}








################################################################################
# EventBridge
################################################################################

# RDSクラスターのイベントを検知
resource "aws_cloudwatch_event_rule" "event_rds_cluster" {
  description   = "CloudWatch Event Rule to send notification on RDS DB Cluster Event."
  event_pattern = <<-PATTERN
    {
      "detail": {
        "EventCategories": [
          "failover",
          "failure",
          "maintenance",
          "recovery",
          "notification"
        ]
      },
      "detail-type": [ "RDS DB Cluster Event" ],
      "resources": [ "${aws_rds_cluster.postgresql.arn}" ],
      "source": [ "aws.rds" ]
    }
  PATTERN
  # state         = "ENABLED"
  name = "${var.name}-event-rds-cluster"
}

# RDSクラスターのイベント用ロググループ
resource "aws_cloudwatch_log_group" "event_rds_cluster_logging" {
  name = "/rds/${var.name}-event-rds-cluster-log-group"
}

# ロググループへの書き込み権限
resource "aws_cloudwatch_log_resource_policy" "event_rds_cluster_logging" {
  policy_name     = "${var.name}-event-rds-cluster-logging-policy"
  policy_document = <<-POLICY
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          "Effect": "Allow",
          "Principal": {
            "Service": [ "events.amazonaws.com", "delivery.logs.amazonaws.com" ]
          },
          "Resource": "${aws_cloudwatch_log_group.event_rds_cluster_logging.arn}:*"
        }
      ]
    }
  POLICY
}

# RDSクラスターのイベントをSNSへ送信
resource "aws_cloudwatch_event_target" "event_rds_cluster_sns" {
  arn  = var.sns_arn
  rule = aws_cloudwatch_event_rule.event_rds_cluster.name
}

# RDSクラスターのイベントをロググループへ書き込み
resource "aws_cloudwatch_event_target" "event_rds_cluster_logging" {
  arn  = aws_cloudwatch_log_group.event_rds_cluster_logging.arn
  rule = aws_cloudwatch_event_rule.event_rds_cluster.name
}



# RDSインスタンスのイベントを検知
resource "aws_cloudwatch_event_rule" "event_rds_instance" {
  description   = "CloudWatch Event Rule to send notification on RDS DB Instance Event."
  event_pattern = <<-PATTERN
    {
      "detail": {
        "EventCategories": [
          "availability",
          "configuration change",
          "deletion",
          "failover",
          "failure",
          "maintenance",
          "notification",
          "recovery"
        ]
      },
      "detail-type": [ "RDS DB Instance Event" ],
      "resources": [
        { "prefix": "arn:aws:rds:${local.region}:${local.account_id}:db:${aws_rds_cluster.postgresql.cluster_identifier}-instance" }
      ],
      "source": [ "aws.rds" ]
    }
  PATTERN

  # state = "ENABLED"
  name = "${var.name}-event-rds-instance"
}

# RDSインスタンスのイベント用ロググループ
resource "aws_cloudwatch_log_group" "event_rds_instance_logging" {
  name = "/rds/${var.name}-event-rds-instance-log-group"
}

# ロググループへの書き込み権限
resource "aws_cloudwatch_log_resource_policy" "event_rds_instance_logging" {
  policy_name     = "${var.name}-event-rds-instance-logging-policy"
  policy_document = <<-POLICY
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          "Effect": "Allow",
          "Principal": {
            "Service": [ "events.amazonaws.com", "delivery.logs.amazonaws.com" ]
          },
          "Resource": "${aws_cloudwatch_log_group.event_rds_instance_logging.arn}:*"
        }
      ]
    }
  POLICY
}

# RDSインスタンスのイベントをSNSへ送信
resource "aws_cloudwatch_event_target" "event_rds_instance_sns" {
  arn  = var.sns_arn
  rule = aws_cloudwatch_event_rule.event_rds_instance.name
}

# RDSインスタンスのイベントをロググループへ書き込み
resource "aws_cloudwatch_event_target" "event_rds_instance_logging" {
  arn  = aws_cloudwatch_log_group.event_rds_instance_logging.arn
  rule = aws_cloudwatch_event_rule.event_rds_instance.name
}
