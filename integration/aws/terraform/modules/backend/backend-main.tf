locals {
  api_family_name                     = "${var.name}-api"
  push_notification_family_name       = "${var.name}-push-notification"
  send_email_notification_family_name = "${var.name}-send-email-notification"
}


#----------------------------------------
# IAMロール
#----------------------------------------
data "aws_iam_policy_document" "assume-role-policy-document" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"
      identifiers = [
        "ecs-tasks.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "ecs-task-execution-role" {
  name               = var.ecs_task_execution_role_name
  assume_role_policy = data.aws_iam_policy_document.assume-role-policy-document.json
}

resource "aws_iam_role_policy_attachment" "ecs-task-execution-role-policy-attachment" {
  role       = aws_iam_role.ecs-task-execution-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs-task-role" {
  name = var.ecs_task_role_name

  assume_role_policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Principal": {
            "Service": "ecs-tasks.amazonaws.com"
          },
          "Effect": "Allow",
          "Sid": ""
        }
      ]
    }
  EOF
}

resource "aws_iam_role_policy" "ecs-task-role-policy" {
  name = "ecs-task-${var.env}-role-policy"
  role = aws_iam_role.ecs-task-role.id

  policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "sns:*"
          ],
          "Effect": "Allow",
          "Resource": "*"
        }
      ]
    }
  EOF
}

resource "aws_iam_role_policy_attachment" "ecs-task-role-s3-policy-attachment" {
  role       = aws_iam_role.ecs-task-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "ecs-task-role-ses-policy-attachment" {
  role       = aws_iam_role.ecs-task-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSESFullAccess"
}

resource "aws_iam_role_policy_attachment" "ecs-task-role-secrets-policy-attachment" {
  role       = aws_iam_role.ecs-task-role.name
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
}





# お知らせ通知機能用EventBridgeロール作成
resource "aws_iam_role" "event_notification_role" {
  name               = "${var.name}-event-notification-role"
  assume_role_policy = <<-POLICY
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "",
          "Effect": "Allow",
          "Principal": {
          "Service": "events.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
        }
      ]
    }
  POLICY
}

# お知らせ通知機能用EventBridgeロールにカスタマーインラインポリシーを追加
# - ECS push_notificationの実行権限
# - ECS send_email_notificationの実行権限
resource "aws_iam_role_policy" "event_notification_role_policy" {
  name = "${var.name}-event-notification-role-policy"
  role = aws_iam_role.event_notification_role.id

  policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "ecs:RunTask",
          "Resource": [
            "${local.push_notification_taskdef_arn_only}:*",
            "${local.push_notification_taskdef_arn_only}",
            "${local.send_email_notification_taskdef_arn_only}:*",
            "${local.send_email_notification_taskdef_arn_only}"
          ],
          "Condition": {
            "ArnLike": {
              "ecs:cluster": "${aws_ecs_cluster.this.arn}"
            }
          }
        },
        {
          "Effect": "Allow",
          "Action": "iam:PassRole",
          "Resource": "*",
          "Condition": {
            "StringLike": {
              "iam:PassedToService": "ecs-tasks.amazonaws.com"
            }
          }
        },
        {
          "Effect": "Allow",
          "Action": "ecs:TagResource",
          "Resource": "*",
          "Condition": {
            "StringEquals": {
              "ecs:CreateAction": [
                "RunTask"
              ]
            }
          }
        }
      ]
    }
  EOF
}




#----------------------------------------
# ECSクラスター
#----------------------------------------
resource "aws_ecs_cluster" "this" {
  name = var.name
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}



#----------------------------------------
# ECSタスクのログ出力先ロググループ
#----------------------------------------
# api
resource "aws_cloudwatch_log_group" "ecs-api" {
  name              = "/ecs/${local.api_family_name}"
  retention_in_days = var.retention_in_days
}

# push_notification
resource "aws_cloudwatch_log_group" "ecs_push_notification" {
  name              = "/ecs/${local.push_notification_family_name}"
  retention_in_days = var.retention_in_days
}

# send_email_notification
resource "aws_cloudwatch_log_group" "ecs_send_email_notification" {
  name              = "/ecs/${local.send_email_notification_family_name}"
  retention_in_days = var.retention_in_days
}



#----------------------------------------
# ECSタスク定義
#----------------------------------------
# api
resource "aws_ecs_task_definition" "api" {
  family = local.api_family_name

  container_definitions = <<-EOF
    [
      {
        "name": "${var.name}-api",
        "image": "${var.api_ecr_endpoint}",
        "command": ${jsonencode(var.command)},
        "cpu": ${var.api_container_cpu},
        "memory": ${var.api_container_memory},
        "portMappings": [
          {
            "containerPort": 80
          }
        ],
        "environment": [
          {
            "name": "DEBUG",
            "value": "${var.debug}"
          },
          {
            "name": "SECRET_KEY",
            "value": "${var.secret_key}"
          },
          {
            "name": "LANGUAGE_CODE",
            "value": "ja-jp"
          },
          {
            "name": "TIME_ZONE",
            "value": "Asia/Tokyo"
          },
          {
            "name": "ALLOWED_HOSTS",
            "value": "*"
          },
          {
            "name": "DATABASE_URL",
            "value": "${var.database_url}"
          },
          {
            "name": "AWS_REGION_NAME",
            "value": "${var.aws_region_name}"
          },
          {
            "name": "AWS_BUCKET_NAME",
            "value": "${var.aws_bucket_name}"
          },
          {
            "name": "EMAIL_SENDER",
            "value": "${var.email_sender}"
          },
          {
            "name": "EMAIL_CONFIRMATION_TTL_IN_DAY",
            "value": "${var.email_confirmation_ttl_in_days}"
          },
          {
            "name": "AWS_SES_CONFIGURATION_SET_NAME",
            "value": "${var.aws_ses_configuration_set_name}"
          },
          {
            "name": "TMP_DIR",
            "value": "${var.tmp_dir}"
          },
          {
            "name": "BASE_URL",
            "value": "${var.base_url}"
          },
          {
            "name": "BACKEND_URL",
            "value": "${var.backend_url}"
          },
          {
            "name": "ECS_TASK_ROLE_NAME",
            "value": "${var.ecs_task_role_name}"
          },
          {
            "name": "CITY_CA_ENDPOINT",
            "value": "${var.city_ca_endpoint}"
          },
          {
            "name": "CITY_CA_APIKEY",
            "value": "${var.city_ca_apikey}"
          },
          {
            "name": "FCS_ENDPOINT",
            "value": "${var.fcs_endpoint}"
          },
          {
            "name": "FCS_APIKEY",
            "value": "${var.fcs_apikey}"
          },
          {
            "name": "MIRAIRO_CONNECT_API_BASE_URL",
            "value": "${var.mirairo_connect_api_base_url}"
          },
          {
            "name": "SNS_ARN",
            "value": "${var.push_notification_arn}"
          },
          {
            "name": "DEFAULT_FILE_STORAGE",
            "value": "${var.default_file_storage}"
          },
          {
            "name": "AWS_STORAGE_BUCKET_NAME",
            "value": "${var.aws_storage_bucket_name}"
          },
          {
            "name": "SITE_DOMAIN",
            "value": "${var.site_domain}"
          },
          {
            "name": "SITE_SUB_DOMAIN",
            "value": "${var.site_sub_domain}"
          },
          {
            "name": "CITY_CA_DISABLE",
            "value": "${var.city_ca_disable}"
          },
          {
            "name": "APP_IS_MAINTENANCE",
            "value": "${var.app_is_maintenance}"
          },
          {
            "name": "HTP_HTML_URL",
            "value": "${var.htp_html_url}"
          },
          {
            "name": "HTP_API_URL",
            "value": "${var.htp_api_url}"
          }
        ],
        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "${aws_cloudwatch_log_group.ecs-api.name}",
            "awslogs-region": "${var.region}",
            "awslogs-stream-prefix": "ecs"
          }
        }
      }
    ]
  EOF

  network_mode       = "awsvpc"
  task_role_arn      = aws_iam_role.ecs-task-role.arn
  execution_role_arn = aws_iam_role.ecs-task-execution-role.arn

  requires_compatibilities = [
    "FARGATE"
  ]

  cpu    = var.api_container_cpu
  memory = var.api_container_memory
}


# push_notification
resource "aws_ecs_task_definition" "push_notification" {
  family = local.push_notification_family_name

  container_definitions = <<-EOF
    [
      {
        "name": "${var.name}-push-notification",
        "image": "${var.api_ecr_endpoint}",
        "command": [
                    "python",
                    "manage.py",
                    "push_notification"
                    ],
        "cpu": 256,
        "memory": 512,
        "environment": [
          {
            "name": "DEBUG",
            "value": "${var.debug}"
          },
          {
            "name": "SECRET_KEY",
            "value": "${var.secret_key}"
          },
          {
            "name": "LANGUAGE_CODE",
            "value": "ja-jp"
          },
          {
            "name": "TIME_ZONE",
            "value": "Asia/Tokyo"
          },
          {
            "name": "ALLOWED_HOSTS",
            "value": "*"
          },
          {
            "name": "DATABASE_URL",
            "value": "${var.database_url}"
          },
          {
            "name": "AWS_REGION_NAME",
            "value": "${var.aws_region_name}"
          },
          {
            "name": "AWS_BUCKET_NAME",
            "value": "${var.aws_bucket_name}"
          },
          {
            "name": "EMAIL_SENDER",
            "value": "${var.email_sender}"
          },
          {
            "name": "EMAIL_CONFIRMATION_TTL_IN_DAY",
            "value": "${var.email_confirmation_ttl_in_days}"
          },
          {
            "name": "AWS_SES_CONFIGURATION_SET_NAME",
            "value": "${var.aws_ses_configuration_set_name}"
          },
          {
            "name": "TMP_DIR",
            "value": "${var.tmp_dir}"
          },
          {
            "name": "BASE_URL",
            "value": "${var.base_url}"
          },
          {
            "name": "BACKEND_URL",
            "value": "${var.backend_url}"
          },
          {
            "name": "ECS_TASK_ROLE_NAME",
            "value": "${var.ecs_task_role_name}"
          },
          {
            "name": "CITY_CA_ENDPOINT",
            "value": "${var.city_ca_endpoint}"
          },
          {
            "name": "CITY_CA_APIKEY",
            "value": "${var.city_ca_apikey}"
          },
          {
            "name": "FCS_ENDPOINT",
            "value": "${var.fcs_endpoint}"
          },
          {
            "name": "FCS_APIKEY",
            "value": "${var.fcs_apikey}"
          },
          {
            "name": "MIRAIRO_CONNECT_API_BASE_URL",
            "value": "${var.mirairo_connect_api_base_url}"
          },
          {
            "name": "SNS_ARN",
            "value": "${var.push_notification_arn}"
          },
          {
            "name": "DEFAULT_FILE_STORAGE",
            "value": "${var.default_file_storage}"
          },
          {
            "name": "AWS_STORAGE_BUCKET_NAME",
            "value": "${var.aws_storage_bucket_name}"
          },
          {
            "name": "SITE_DOMAIN",
            "value": "${var.site_domain}"
          },
          {
            "name": "SITE_SUB_DOMAIN",
            "value": "${var.site_sub_domain}"
          },
          {
            "name": "CITY_CA_DISABLE",
            "value": "${var.city_ca_disable}"
          },
          {
            "name": "APP_IS_MAINTENANCE",
            "value": "${var.app_is_maintenance}"
          },
          {
            "name": "HTP_HTML_URL",
            "value": "${var.htp_html_url}"
          },
          {
            "name": "HTP_API_URL",
            "value": "${var.htp_api_url}"
          }
        ],
        "readonlyRootFilesystem": true,
        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "${aws_cloudwatch_log_group.ecs_push_notification.name}",
            "awslogs-region": "${var.region}",
            "awslogs-stream-prefix": "ecs"
          }
        }
      }
    ]
  EOF

  network_mode       = "awsvpc"
  task_role_arn      = aws_iam_role.ecs-task-role.arn
  execution_role_arn = aws_iam_role.ecs-task-execution-role.arn

  requires_compatibilities = [
    "FARGATE"
  ]

  cpu    = 256
  memory = 512
}



# send_email_notification
resource "aws_ecs_task_definition" "send_email_notification" {
  family = local.send_email_notification_family_name

  container_definitions = <<-EOF
    [
      {
        "name": "${var.name}-send-email-notification",
        "image": "${var.api_ecr_endpoint}",
        "command": [
                    "python",
                    "manage.py",
                    "send_email_notification"
                    ],
        "cpu": 256,
        "memory": 512,
        "environment": [
          {
            "name": "DEBUG",
            "value": "${var.debug}"
          },
          {
            "name": "SECRET_KEY",
            "value": "${var.secret_key}"
          },
          {
            "name": "LANGUAGE_CODE",
            "value": "ja-jp"
          },
          {
            "name": "TIME_ZONE",
            "value": "Asia/Tokyo"
          },
          {
            "name": "ALLOWED_HOSTS",
            "value": "*"
          },
          {
            "name": "DATABASE_URL",
            "value": "${var.database_url}"
          },
          {
            "name": "AWS_REGION_NAME",
            "value": "${var.aws_region_name}"
          },
          {
            "name": "AWS_BUCKET_NAME",
            "value": "${var.aws_bucket_name}"
          },
          {
            "name": "EMAIL_SENDER",
            "value": "${var.email_sender}"
          },
          {
            "name": "EMAIL_CONFIRMATION_TTL_IN_DAY",
            "value": "${var.email_confirmation_ttl_in_days}"
          },
          {
            "name": "AWS_SES_CONFIGURATION_SET_NAME",
            "value": "${var.aws_ses_configuration_set_name}"
          },
          {
            "name": "TMP_DIR",
            "value": "${var.tmp_dir}"
          },
          {
            "name": "BASE_URL",
            "value": "${var.base_url}"
          },
          {
            "name": "BACKEND_URL",
            "value": "${var.backend_url}"
          },
          {
            "name": "ECS_TASK_ROLE_NAME",
            "value": "${var.ecs_task_role_name}"
          },
          {
            "name": "CITY_CA_ENDPOINT",
            "value": "${var.city_ca_endpoint}"
          },
          {
            "name": "CITY_CA_APIKEY",
            "value": "${var.city_ca_apikey}"
          },
          {
            "name": "FCS_ENDPOINT",
            "value": "${var.fcs_endpoint}"
          },
          {
            "name": "FCS_APIKEY",
            "value": "${var.fcs_apikey}"
          },
          {
            "name": "MIRAIRO_CONNECT_API_BASE_URL",
            "value": "${var.mirairo_connect_api_base_url}"
          },
          {
            "name": "SNS_ARN",
            "value": "${var.push_notification_arn}"
          },
          {
            "name": "DEFAULT_FILE_STORAGE",
            "value": "${var.default_file_storage}"
          },
          {
            "name": "AWS_STORAGE_BUCKET_NAME",
            "value": "${var.aws_storage_bucket_name}"
          },
          {
            "name": "SITE_DOMAIN",
            "value": "${var.site_domain}"
          },
          {
            "name": "SITE_SUB_DOMAIN",
            "value": "${var.site_sub_domain}"
          },
          {
            "name": "CITY_CA_DISABLE",
            "value": "${var.city_ca_disable}"
          },
          {
            "name": "APP_IS_MAINTENANCE",
            "value": "${var.app_is_maintenance}"
          },
          {
            "name": "HTP_HTML_URL",
            "value": "${var.htp_html_url}"
          },
          {
            "name": "HTP_API_URL",
            "value": "${var.htp_api_url}"
          }
        ],
        "readonlyRootFilesystem": true,
        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "${aws_cloudwatch_log_group.ecs_send_email_notification.name}",
            "awslogs-region": "${var.region}",
            "awslogs-stream-prefix": "ecs"
          }
        }
      }
    ]
  EOF

  network_mode       = "awsvpc"
  task_role_arn      = aws_iam_role.ecs-task-role.arn
  execution_role_arn = aws_iam_role.ecs-task-execution-role.arn

  requires_compatibilities = [
    "FARGATE"
  ]

  cpu    = 256
  memory = 512
}





#----------------------------------------
# ECSサービス
#----------------------------------------
# デプロイ時にリビジョンが更新されるため、最新のrevisionをdataで取得
data "aws_ecs_task_definition" "api" {
  task_definition = aws_ecs_task_definition.api.family
}

# apiサービス
resource "aws_ecs_service" "api" {
  name                              = local.api_family_name
  launch_type                       = "FARGATE"
  platform_version                  = var.ecs_platform_version
  cluster                           = aws_ecs_cluster.this.id
  task_definition                   = data.aws_ecs_task_definition.api.arn # デプロイ時にリビジョンが更新されるため、最新のrevisionをdataで取得
  desired_count                     = var.ecs_task_number
  enable_execute_command            = "true"
  health_check_grace_period_seconds = 300
  load_balancer {
    target_group_arn = var.target_group.arn
    container_name   = "${var.name}-api"
    container_port   = 80
  }
  network_configuration {
    subnets = var.private_subnets
    security_groups = [
      var.security_group.id
    ]
  }
  # lifecycle {
  #   ignore_changes = [
  #     task_definition
  #   ]
  # }
  depends_on = [aws_ecs_task_definition.api]
}

resource "aws_appautoscaling_target" "api" {
  service_namespace  = "ecs"
  resource_id        = "service/${var.name}/${local.api_family_name}"
  scalable_dimension = "ecs:service:DesiredCount"
  min_capacity       = var.min_capacity
  max_capacity       = var.max_capacity
}

resource "aws_appautoscaling_policy" "api" {
  name               = "${var.name}-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.api.resource_id
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = aws_appautoscaling_target.api.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 40
    scale_in_cooldown  = 30
    scale_out_cooldown = 300
  }
  depends_on = [
    aws_appautoscaling_target.api,
    aws_ecs_service.api
  ]
}





#----------------------------------------
# ECSイベントスケジュール
#----------------------------------------
locals {
  # 常に最新のを参照する。
  # https://github.com/hashicorp/terraform-provider-aws/issues/6840
  push_notification_taskdef_arn_only       = replace(aws_ecs_task_definition.push_notification.arn, "/:\\d+$/", "")
  send_email_notification_taskdef_arn_only = replace(aws_ecs_task_definition.send_email_notification.arn, "/:\\d+$/", "")
}

# お知らせ通知機能用スケジュールタスク
resource "aws_cloudwatch_event_rule" "event_notification" {
  name                = "${var.name}-event-notification"
  schedule_expression = var.notification_event_schedule
}

# push_notification
resource "aws_cloudwatch_event_target" "push_notification" {
  target_id = local.push_notification_family_name
  arn       = aws_ecs_cluster.this.arn
  rule      = aws_cloudwatch_event_rule.event_notification.name
  role_arn  = aws_iam_role.event_notification_role.arn
  ecs_target {
    launch_type         = "FARGATE"
    task_definition_arn = local.push_notification_taskdef_arn_only
    platform_version    = "LATEST"
    propagate_tags      = "TASK_DEFINITION"
    network_configuration {
      subnets          = var.private_subnets
      security_groups  = ["${var.security_group.id}"]
      assign_public_ip = false
    }
  }
}

# send_email_notification
resource "aws_cloudwatch_event_target" "send_email_notification" {
  target_id = local.send_email_notification_family_name
  arn       = aws_ecs_cluster.this.arn
  rule      = aws_cloudwatch_event_rule.event_notification.name
  role_arn  = aws_iam_role.event_notification_role.arn
  ecs_target {
    launch_type         = "FARGATE"
    task_definition_arn = local.send_email_notification_taskdef_arn_only
    platform_version    = "LATEST"
    propagate_tags      = "TASK_DEFINITION"
    network_configuration {
      subnets          = var.private_subnets
      security_groups  = ["${var.security_group.id}"]
      assign_public_ip = false
    }
  }
}





#----------------------------------------
# 監視設定
#----------------------------------------

# apiコンテナアプリケーションログ監視（クリティカル検知）
resource "aws_cloudwatch_log_metric_filter" "ecs_log_filter_for_api_critical" {
  name           = "${var.name}-ecs-log-filter-for-api-critical"
  pattern        = "?CRITICAL ?Critical ?critical"
  log_group_name = aws_cloudwatch_log_group.ecs-api.name
  metric_transformation {
    namespace = "LogMetrics"
    name      = "${var.name}-ECSLogForApiCriticalCount"
    value     = "1"
  }
}
resource "aws_cloudwatch_metric_alarm" "ecs_log_filter_for_api_critical" {
  actions_enabled     = "true"
  alarm_actions       = [var.sns_arn]
  alarm_description   = "Application Log Critical Alarm"
  alarm_name          = "${var.name}-ecs-log-filter-for-api-critical-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.ecs_log_filter_for_api_critical.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.ecs_log_filter_for_api_critical.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "notBreaching"
}



# apiコンテナアプリケーションログ監視（エラー検知）
resource "aws_cloudwatch_log_metric_filter" "ecs_log_filter_for_api_error" {
  name           = "${var.name}-ecs-log-filter-for-api-error"
  pattern        = "[( msg=\"*ERROR*\" || msg=\"*Error*\" || msg=\"*error*\" ) && ( msg!=\"*token is None...*\" && msg!=\"*token is invalid...*\" )]"
  log_group_name = aws_cloudwatch_log_group.ecs-api.name
  metric_transformation {
    namespace = "LogMetrics"
    name      = "${var.name}-ECSLogForApiErrorCount"
    value     = "1"
  }
}
resource "aws_cloudwatch_metric_alarm" "ecs_log_filter_for_api_error" {
  actions_enabled     = "true"
  alarm_actions       = [var.sns_arn]
  alarm_description   = "Application Log Error Alarm"
  alarm_name          = "${var.name}-ecs-log-filter-for-api-error-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.ecs_log_filter_for_api_error.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.ecs_log_filter_for_api_error.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "notBreaching"
}



# # apiコンテナアプリケーションログ監視（ワーニング検知）
# resource "aws_cloudwatch_log_metric_filter" "ecs_log_filter_for_api_warn" {
#   name           = "${var.name}-ecs-log-filter-for-api-warn"
#   pattern        = "?WARN ?Warn ?warn"
#   log_group_name = aws_cloudwatch_log_group.ecs-api.name
#   metric_transformation {
#     namespace = "LogMetrics"
#     name      = "${var.name}-ECSLogForApiWarnCount"
#     value     = "1"
#   }
# }
# resource "aws_cloudwatch_metric_alarm" "ecs_log_filter_for_api_warn" {
#   actions_enabled     = "true"
#   alarm_actions       = [var.sns_arn]
#   alarm_description   = "Application Log Warn Alarm"
#   alarm_name          = "${var.name}-ecs-log-filter-for-api-warn-alarm"
#   comparison_operator = "GreaterThanOrEqualToThreshold"
#   datapoints_to_alarm = "1"
#   evaluation_periods  = "1"
#   metric_name         = aws_cloudwatch_log_metric_filter.ecs_log_filter_for_api_warn.metric_transformation[0].name
#   namespace           = aws_cloudwatch_log_metric_filter.ecs_log_filter_for_api_warn.metric_transformation[0].namespace
#   period              = "300"
#   statistic           = "Sum"
#   threshold           = "1"
#   treat_missing_data  = "notBreaching"
# }
