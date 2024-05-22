# https の証明書は ACM で作成・管理する
module "acm" {
  source = "../../modules/acm"

  create_cert_for_cloudfront = var.create_cert_for_cloudfront
  create_cert_route53_record = var.create_cert_route53_record
  route53_zone_id            = var.route53_zone_id
  domain_name                = var.domain_name
  backend_domain             = var.backend_domain
  temp_url_domain            = var.temp_url_domain
  providers = {
    aws.cloudfront_region = aws.us-east-1
  }
}

# VPC, subnet, NAT gateway など
module "network" {
  source = "../../modules/network"

  name     = "${var.name}-${var.env}"
  region   = var.region
  vpc_cidr = var.vpc_cidr

  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets

  db_port          = var.db_port
  bastion_ami      = var.bastion_ami
  bastion_key_pair = var.bastion_key_pair

  retention_in_days = var.vpc_log_retention_in_days
  allow_ips         = var.white_ip_addresses_for_admin
}

# ALB, listener rule など
module "route" {
  source = "../../modules/route"

  name                         = "${var.name}-${var.env}"
  security_group               = module.network.security_group_lb
  public_subnets               = module.network.public_subnets
  access_log_bucket            = var.access_log_bucket
  access_log_enabled           = var.access_log_enabled
  vpc                          = module.network.vpc
  acm_arn                      = module.acm.cert_for_backend.arn
  route53_zone_id              = var.route53_zone_id
  frontend_domain              = var.frontend_domain
  cdn                          = module.frontend.cdn
  backend_domain               = var.backend_domain
  white_ip_addresses_for_admin = var.white_ip_addresses_for_admin
  temp_url_domain              = var.temp_url_domain
  cdn_for_temp_url             = module.frontend.cdn_for_temp_url
}

module "database" {
  source = "../../modules/database"

  name                   = "${var.name}-${var.env}"
  private_subnets        = module.network.private_subnets
  availability_zones     = var.availability_zones
  db_master_name         = var.db_master_name
  db_master_user         = var.db_master_user
  db_master_password     = var.db_master_password
  security_group         = module.network.security_group_db
  monitoring_interval    = var.monitoring_interval
  monitoring_role_arn    = var.monitoring_role_arn
  monitoring_role_name   = var.monitoring_role_name
  create_monitoring_role = var.create_monitoring_role
  aurora_engine_version  = var.aurora_engine_version
  sns_arn                = module.chatbot_monitor_channel.sns_topic_chatbot.arn
}

module "frontend" {
  source = "../../modules/frontend"

  env  = var.env
  name = "${var.name}-${var.env}"

  frontend_bucket    = "${var.env}.${var.name}.jp"
  frontend_domain    = var.frontend_domain
  acm_arn            = var.create_cert_for_cloudfront ? module.acm.cert_for_cloudfront.arn : var.acm_arn
  backend_domain     = var.backend_domain
  log_bucket         = var.log_bucket
  white_ip_addresses = var.white_ip_addresses
  providers = {
    aws.cloudfront_region = aws.us-east-1
  }

  temp_url_acm_arn = module.acm.cert_for_cloudfront_temp_url.arn
  temp_url_waf_arn = module.waf_cloudfront_for_temp_url.waf_arn
  temp_url_domain  = var.temp_url_domain
}

module "backend" {
  source = "../../modules/backend"

  env  = var.env
  name = "${var.name}-${var.env}"

  ecs_task_execution_role_name   = var.ecs_task_execution_role_name
  ecs_task_role_name             = var.ecs_task_role_name
  city_ca_endpoint               = var.city_ca_endpoint
  city_ca_apikey                 = var.city_ca_apikey
  fcs_endpoint                   = var.fcs_endpoint
  fcs_apikey                     = var.fcs_apikey
  mirairo_connect_api_base_url   = var.mirairo_connect_api_base_url
  sns_arn                        = module.chatbot_monitor_channel.sns_topic_chatbot.arn
  push_notification_arn          = var.push_notification_arn #プッシュ通知用のSNSのARN
  api_ecr_endpoint               = "${var.api_ecr_endpoint}:${var.image_tag}"
  command                        = var.command
  debug                          = var.debug
  secret_key                     = var.secret_key
  aws_region_name                = var.aws_region_name
  aws_bucket_name                = var.aws_bucket_name
  email_sender                   = var.email_sender
  email_confirmation_ttl_in_days = var.email_confirmation_ttl_in_days
  aws_ses_configuration_set_name = var.aws_ses_configuration_set_name
  tmp_dir                        = var.tmp_dir
  base_url                       = "https://${var.frontend_domain}"
  backend_url                    = var.backend_url
  region                         = var.region
  database_url                   = "${var.database_url_prefix}:${var.db_master_password}@${module.database.database.endpoint}/${var.database_url_suffix}"
  db_address                     = module.database.database.endpoint
  db_name                        = var.db_name
  db_user                        = var.db_master_user
  db_password                    = var.db_master_password
  db_port                        = var.db_port
  ecs_platform_version           = var.ecs_platform_version
  ecs_task_number                = var.ecs_task_number
  target_group                   = module.route.target_group
  private_subnets                = module.network.private_subnets
  security_group                 = module.network.security_group_ecs
  min_capacity                   = var.min_capacity
  max_capacity                   = var.max_capacity
  api_container_cpu              = var.api_container_cpu
  api_container_memory           = var.api_container_memory
  retention_in_days              = var.ecs_log_retention_in_days
  default_file_storage           = var.default_file_storage
  aws_storage_bucket_name        = var.aws_storage_bucket_name
  site_domain                    = var.site_domain
  site_sub_domain                = var.site_sub_domain
  city_ca_disable                = var.city_ca_disable
  app_is_maintenance             = var.app_is_maintenance
  htp_html_url                   = var.htp_html_url
  htp_api_url                    = var.htp_api_url
  notification_event_schedule    = var.notification_event_schedule
}

module "s3" {
  source = "../../modules/s3"

  name = "${var.name}-${var.env}"
}

// メール
module "ses" {
  source = "../../modules/ses"

  name = "${var.name}-${var.env}"
}

// アラート
module "cloudwatch" {
  source = "../../modules/cloudwatch"

  name    = "${var.name}-${var.env}"
  sns_arn = module.chatbot_monitor_channel.sns_topic_chatbot.arn
  ecs_alarms = tolist([
    {
      alarm_name          = "${var.name}-${var.env}-ecs-cpu-utilization-high"
      comparison_operator = "GreaterThanOrEqualToThreshold"
      evaluation_periods  = 2
      threshold           = 40 # AutoScalingのしきい値と同値を設定
      alarm_description   = "${var.name}-${var.env}-cpu-utilization-high"
      metric_name         = "CPUUtilization"
      namespace           = "AWS/ECS"
      period              = "60"
      statistic           = "Average"
      dimensions = {
        "ClusterName" = "${var.name}-${var.env}"
        "ServiceName" = "${var.name}-${var.env}-api"
      }
    },
    {
      alarm_name          = "${var.name}-${var.env}-ecs-memory-utilization-high"
      comparison_operator = "GreaterThanOrEqualToThreshold"
      evaluation_periods  = 2
      threshold           = 1024
      alarm_description   = "${var.name}-${var.env}-memory-utilization-high"
      metric_name         = "MemoryUtilized"
      namespace           = "ECS/ContainerInsights"
      period              = "60"
      statistic           = "Average"
      dimensions = {
        "ClusterName" = "${var.name}-${var.env}"
        "ServiceName" = "${var.name}-${var.env}-api"
      }
    },
    {
      alarm_name          = "${var.name}-${var.env}-ecs-desired-task-count-low"
      comparison_operator = "LessThanThreshold"
      evaluation_periods  = 2
      threshold           = var.min_capacity # ECSタスクの最小値を設定
      alarm_description   = "${var.name}-${var.env}-ecs-desired-task-count-low"
      metric_name         = "DesiredTaskCount"
      namespace           = "ECS/ContainerInsights"
      period              = "60"
      statistic           = "Average"
      dimensions = {
        "ClusterName" = "${var.name}-${var.env}"
        "ServiceName" = "${var.name}-${var.env}-api"
      }
    }
  ])

  rds_alarms = tolist([
    {
      alarm_name          = "${var.name}-${var.env}-rds-cpu-utilization-high"
      comparison_operator = "GreaterThanOrEqualToThreshold"
      evaluation_periods  = 2
      threshold           = 60
      alarm_description   = "${var.name}-${var.env}-rds-cpu-utilization-high"
      metric_name         = "CPUUtilization"
      namespace           = "AWS/RDS"
      period              = "60"
      statistic           = "Average"
    },
    {
      alarm_name          = "${var.name}-${var.env}-rds-freeable-memory-low"
      comparison_operator = "LessThanThreshold"
      evaluation_periods  = 2
      threshold           = 2048
      alarm_description   = "${var.name}-${var.env}-rds-freeable-memory-low"
      metric_name         = "FreeableMemory"
      namespace           = "AWS/RDS"
      period              = "60"
      statistic           = "Average"
    },
    {
      alarm_name          = "${var.name}-${var.env}-rds-free-storage-space-low"
      comparison_operator = "LessThanThreshold"
      evaluation_periods  = 2
      threshold           = 2048
      alarm_description   = "${var.name}-${var.env}-rds-free-storage-space-low"
      metric_name         = "FreeStorageSpace"
      namespace           = "AWS/RDS"
      period              = "60"
      statistic           = "Average"
    },
  ])

  alb_alarms = tolist([
    {
      alarm_name          = "${var.name}-${var.env}-target-group-http-5xx-count"
      comparison_operator = "GreaterThanOrEqualToThreshold"
      evaluation_periods  = 2
      threshold           = 0
      alarm_description   = "${var.name}-${var.env}-target-group-http-5xx-count"
      metric_name         = "HTTPCode_Target_5XX_Count"
      namespace           = "AWS/ApplicationELB"
      period              = "60"
      statistic           = "Sum"
      dimensions = {
        "TargetGroup"  = module.route.target_group.arn
        "LoadBalancer" = module.route.alb.arn
      }
    },
    {
      alarm_name          = "${var.name}-${var.env}-alb-http-5xx-count"
      comparison_operator = "GreaterThanOrEqualToThreshold"
      evaluation_periods  = 2
      threshold           = 0
      alarm_description   = "${var.name}-${var.env}-alb-http-5xx-count"
      metric_name         = "HTTPCode_ELB_5XX_Count"
      namespace           = "AWS/ApplicationELB"
      period              = "60"
      statistic           = "Sum"
      dimensions = {
        "LoadBalancer" = module.route.alb.arn
      }
    },
    {
      alarm_name          = "${var.name}-${var.env}-target-group-response-time-high"
      comparison_operator = "GreaterThanOrEqualToThreshold"
      evaluation_periods  = 2
      threshold           = 10
      alarm_description   = "${var.name}-${var.env}-target-group-response-time-high"
      metric_name         = "TargetResponseTime"
      namespace           = "AWS/ApplicationELB"
      period              = "60"
      statistic           = "Average"
      dimensions = {
        "TargetGroup"  = module.route.target_group.arn
        "LoadBalancer" = module.route.alb.arn
      }
    }
  ])
}


module "waf_cloudfront_for_temp_url" {
  source = "../../modules/waf"

  prefix          = "${var.name}-${var.env}-temp-url"
  allowed_ip_list = var.allowed_ip_list_for_temp_url
  providers = {
    aws = aws.us-east-1
  }
}


module "chatbot_monitor_channel" {
  source = "../../modules/chatbot"

  prefix             = "${var.name}-${var.env}"
  slack_workspace_id = var.slack_workspace_id
  slack_channel_id   = var.slack_channel_id_monitor
  notification_type  = var.notification_type_monitor
}

