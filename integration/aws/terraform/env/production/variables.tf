variable "aws_profile" {
  type    = string
  default = "lg-pwd"
}

// システム名
variable "name" {
  type    = string
  default = "lg-pwd"
}
variable "env" {
  type    = string
  default = "production"
}

variable "region" {
  type    = string
  default = "ap-northeast-1"
}
variable "availability_zones" {
  type    = list(string)
  default = ["ap-northeast-1a", "ap-northeast-1c", "ap-northeast-1d"]
}

variable "vpc_cidr" {
  type    = string
  default = "10.2.0.0/16"
}
variable "public_subnets" {
  type = map(string)
  default = {
    ap-northeast-1a = "10.2.21.0/24"
    ap-northeast-1c = "10.2.23.0/24"
  }
}
variable "private_subnets" {
  type = map(string)
  default = {
    ap-northeast-1a = "10.2.11.0/24"
    ap-northeast-1c = "10.2.13.0/24"
  }
}

variable "bastion_ami" {
  type = string
  // Amazon Linux 2 AMI (x86 64bit)
  default = "ami-0b276ad63ba2d6009"
}
variable "bastion_key_pair" {
  type    = string
  default = "lg-pwd-bastion"
}

variable "access_log_bucket" {
  type    = string
  default = "milabo.lg-pwd.alb.prd"
}
variable "access_log_enabled" {
  type    = bool
  default = true
}

variable "create_cert_for_cloudfront" {
  type    = bool
  default = true
}
// ↑ create を false にするなら既存の証明書の arn を設定する
variable "acm_arn" {
  type    = string
  default = null
}
variable "create_cert_route53_record" {
  type    = bool
  default = true
}
variable "domain_name" {
  type    = string
  default = "lg-pwd.jp"
}
//variable "acm_arn" {}
//variable "acm_arn_useast" {}

// 必須 /0-9A-Z+/
variable "route53_zone_id" {
  type = string
}

// 必須 ["xxx.xxx.xxx.xxx/32"]
variable "white_ip_addresses_for_admin" {
  type = list(string)
}

variable "database_url_prefix" {
  type    = string
  default = "postgresql://lgpwd"
}
variable "database_url_suffix" {
  type    = string
  default = "lgpwd"
}
variable "db_master_name" {
  type    = string
  default = "lgpwd"
}
variable "db_master_user" {
  type    = string
  default = "lgpwd"
}
variable "aurora_engine_version" {
  type = string
}
// 必須
variable "db_master_password" {}
variable "db_name" {
  type    = string
  default = "lgpwd"
}
variable "db_port" {
  type    = string
  default = "5432"
}
variable "monitoring_interval" {
  type    = number
  default = 60
}
variable "monitoring_role_arn" {
  type    = string
  default = null
}
// ロールを予め作っておく必要がある
variable "monitoring_role_name" {
  type    = string
  default = "LgPwdRdsMonitoringPrdRole"
}
variable "create_monitoring_role" {
  type    = bool
  default = true
}
variable "default_file_storage" {
  type    = string
  default = "storages.backends.s3boto3.S3Boto3Storage"
}
variable "aws_storage_bucket_name" {}
variable "site_domain" {
  type    = string
  default = "https://lg-pwd.jp"
}
variable "site_sub_domain" {
  type    = string
  default = "https://backend.lg-pwd.jp"
}
variable "city_ca_disable" {
  type    = bool
  default = false
}
variable "app_is_maintenance" {
  type    = bool
  default = false
}
variable "htp_html_url" {
  type    = string
  default = "https://temp.lg-pwd.jp/index.html"
}
variable "htp_api_url" {
  type    = string
  default = "https://api.htp.ms.mila-e.jp/html-to-pdf"
}
variable "notification_event_schedule" {
  type = string
}
// 必須 "1.4.0"
variable "ecs_platform_version" {}
// 必須 1 desired_count の初期値のこと
variable "ecs_task_number" {}
// 必須 1 autoscaling の最小タスク数
variable "min_capacity" {}
// 必須 2 autoscaling の最大タスク数
variable "max_capacity" {}
// 必須 1024
variable "api_container_cpu" {}
// 必須 2048
variable "api_container_memory" {}
// 必須 30 ログ記録日数
variable "ecs_log_retention_in_days" {}
variable "vpc_log_retention_in_days" {}

// 必須 予約システムAPIエンドポイント
variable "city_ca_endpoint" {}
variable "city_ca_apikey" {}

// 必須 FCS(混雑状況)のAPIエンドポイント
variable "fcs_endpoint" {}
variable "fcs_apikey" {}

// 必須 ミライロID APIエンドポイント
variable "mirairo_connect_api_base_url" {}

// 必須 プッシュ通知SNSARN
variable "push_notification_arn" {}

variable "frontend_domain" {
  type    = string
  default = "lg-pwd.jp"
}
variable "backend_domain" {
  type    = string
  default = "backend.lg-pwd.jp"
}
variable "temp_url_domain" {
  type    = string
  default = "temp.lg-pwd.jp"
}
variable "log_bucket" {
  type    = string
  default = "milabo.lg-pwd.systemfiles.s3.amazonaws.com"
}
// メンテナンスモードでも接続を許可するIPアドレス(カンマ区切り)
variable "white_ip_addresses" {
  type    = string
  default = ""
}
// ロールを予め作っておく必要がある
// ECS コンテナ管理側のロール (ECR とかログ出力の権限が必要)
variable "ecs_task_execution_role_name" {
  type    = string
  default = "LgPwdEcsTaskExecutionPrdRole"
}
// ロールを予め作っておく必要がある
// ECS コンテナ内部のロール（アプリケーションで使う権限が必要）
variable "ecs_task_role_name" {
  type    = string
  default = "LgPwdEcsTaskPrdRole"
}
// backend のコンテナイメージタグ
variable "image_tag" {
  type    = string
  default = "latest"
}
// 以下は backend コンテナの設定
variable "command" {
  type = list(string)
  default = [
    "gunicorn",
    "config.wsgi",
    "-b",
    "0.0.0.0:80",
    "-w",
    "2",
    "--threads",
    "1",
    "--log-level=info",
    "--max-requests",
    "500",
    "--max-requests-jitter",
    "200",
    "--worker-tmp-dir=/dev/shm"
  ]
}
// 必須 "***.dkr.ecr.ap-northeast-1.amazonaws.com/milabo/***"
variable "api_ecr_endpoint" {}
variable "debug" {
  type    = bool
  default = false
}
// 必須
variable "secret_key" {}
variable "aws_region_name" {
  type    = string
  default = "ap-northeast-1"
}
variable "aws_bucket_name" {
  type    = string
  default = "milabo.lg-pwd.systemfiles"
}
variable "email_sender" {
  type    = string
  default = "info@lg-pwd.jp"
}
variable "email_confirmation_ttl_in_days" {
  type    = number
  default = 1
}
variable "aws_ses_configuration_set_name" {
  type    = string
  default = "lg-pwd-production-configuration-set"
}
variable "tmp_dir" {
  type    = string
  default = "/tmp/lg-pwd"
}
variable "backend_url" {
  type    = string
  default = "https://api.lg-pwd.jp"
}

variable "allowed_ip_list_for_temp_url" {
  type = list(string)
}

variable "slack_workspace_id" {}
variable "slack_channel_id_monitor" {}
variable "notification_type_monitor" {}
