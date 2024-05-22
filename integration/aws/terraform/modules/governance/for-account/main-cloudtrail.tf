# 環境情報取得用データソース
data "aws_caller_identity" "current" {}


#----------------------------------------
# KMS
#----------------------------------------

# CloudTrail用のKMSキー
resource "aws_kms_key" "trail_key" {
  description             = "${var.prefix}-kms-key-for-cloudtrail"
  deletion_window_in_days = 10
  policy                  = data.aws_iam_policy_document.trail_key.json
  enable_key_rotation     = true
}


# CloudTrail用のKMSキーエイリアス
resource "aws_kms_alias" "trail_key" {
  name          = "alias/${var.prefix}-kms-key-for-cloudtrail"
  target_key_id = aws_kms_key.trail_key.key_id
}


# CloudTrail用のKMSキーポリシー
data "aws_iam_policy_document" "trail_key" {
  # Enable IAM User Permissions
  statement {
    effect  = "Allow"
    actions = ["kms:*", ]
    principals {
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root", ]
      type        = "AWS"
    }
    resources = ["*", ]
  }

  # Allow CloudTrail to encrypt logs
  statement {
    effect  = "Allow"
    actions = ["kms:GenerateDataKey*", ]
    condition {
      test = "StringLike"
      values = [
        "arn:aws:cloudtrail:*:${data.aws_caller_identity.current.account_id}:trail/*",
      ]
      variable = "kms:EncryptionContext:aws:cloudtrail:arn"
    }
    principals {
      identifiers = ["cloudtrail.amazonaws.com", ]
      type        = "Service"
    }
    resources = ["*", ]
  }

  # Allow CloudTrail to describe key
  statement {
    effect  = "Allow"
    actions = ["kms:DescribeKey", ]
    principals {
      identifiers = ["cloudtrail.amazonaws.com", ]
      type        = "Service"
    }
    resources = ["*", ]
  }

  # Allow principals in the account to decrypt log files
  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
      "kms:ReEncryptFrom"
    ]
    condition {
      test = "StringLike"
      values = [
        "arn:aws:cloudtrail:*:${data.aws_caller_identity.current.account_id}:trail/*",
      ]
      variable = "kms:EncryptionContext:aws:cloudtrail:arn"
    }
    condition {
      test = "StringEquals"
      values = [
        data.aws_caller_identity.current.account_id,
      ]
      variable = "kms:CallerAccount"
    }
    principals {
      identifiers = ["*", ]
      type        = "AWS"
    }
    resources = ["*", ]
  }
}





#----------------------------------------
# CloudTrail出力用バケット
#----------------------------------------

# CloudTrail格納用バケット
resource "aws_s3_bucket" "trail_bucket" {
  # logを先頭にすることでソートした際にログ関連のS3がまとまって表示される
  bucket = "${var.prefix}-log-cloudtrail"
  # force_destroy = true
}


# CloudTrail格納用バケットポリシー
data "aws_iam_policy_document" "trail_bucket" {
  statement {
    sid    = "AWSCloudTrailAclCheck"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
    actions   = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.trail_bucket.arn]
  }

  statement {
    sid    = "AWSCloudTrailWrite"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.trail_bucket.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*"]
    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }
  }

  # s3-bucket-ssl-requests-only準拠のため、暗号化されている通信のみを許可する
  statement {
    sid    = "AllowSSLRequestsOnly"
    effect = "Deny"
    actions = [
      "s3:*",
    ]
    resources = [
      "${aws_s3_bucket.trail_bucket.arn}",
      "${aws_s3_bucket.trail_bucket.arn}/*",
    ]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}


# バケットバージョニングを有効化
resource "aws_s3_bucket_versioning" "trail_bucket" {
  bucket = aws_s3_bucket.trail_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# CloudTrailのような小さいファイルはGLACIER移行時のコストが高いため転送をやめる
# https://dev.classmethod.jp/articles/explore-breakeven-points-when-migrating-cloudtrail-trail-data-to-glacier-in-s3-lifecycles/
# # ライフサイクルポリシーを設定
# resource "aws_s3_bucket_lifecycle_configuration" "trail_bucket" {
#   bucket = aws_s3_bucket.trail_bucket.id
#   rule {
#     id     = "trail-lifecycle-rules"
#     status = "Enabled"
#     # 370日経過したログはGlacierへ転送する
#     transition {
#       days          = 370
#       storage_class = "GLACIER"
#     }
#   }
# }


# CloudTrail格納用バケットへバケットポリシーをアタッチ
resource "aws_s3_bucket_policy" "trail_bucket" {
  bucket = aws_s3_bucket.trail_bucket.id
  policy = data.aws_iam_policy_document.trail_bucket.json
}

# CloudTrailアクセスログ格納用バケット
resource "aws_s3_bucket" "trail_accesslog_bucket" {
  # logを先頭にすることでソートした際にログ関連のS3がまとまって表示される
  bucket = "${var.prefix}-log-cloudtrail-accesslog"

  # force_destroy = true
}

# CloudTrailアクセスログ格納用バケットACL無効 (バケット所有者の強制)
resource "aws_s3_bucket_ownership_controls" "trail_accesslog_bucket" {
  bucket = aws_s3_bucket.trail_accesslog_bucket.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# CloudTrailアクセスログ格納用バケットのパブリックアクセス
resource "aws_s3_bucket_public_access_block" "trail_accesslog_bucket" {
  bucket                  = aws_s3_bucket.trail_accesslog_bucket.bucket
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# CloudTrailアクセスログ格納用バケットのライフサイクルポリシー
resource "aws_s3_bucket_lifecycle_configuration" "trail_accesslog_bucket" {
  bucket = aws_s3_bucket.trail_accesslog_bucket.id
  rule {
    id     = "expiration-rule"
    status = "Enabled"
    expiration {
      days = 365
    }
  }
}

# CloudTrailアクセスログ格納用バケットバケットポリシー
resource "aws_s3_bucket_policy" "trail_accesslog_bucket" {
  bucket = aws_s3_bucket.trail_accesslog_bucket.id
  policy = <<-POLICY
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowSSLRequestsOnly",
          "Effect": "Deny",
          "Principal": "*",
          "Action": "s3:*",
          "Resource": [
            "${aws_s3_bucket.trail_accesslog_bucket.arn}",
            "${aws_s3_bucket.trail_accesslog_bucket.arn}/*"
          ],
          "Condition": {
            "Bool": {
              "aws:SecureTransport": "false"
            }
          }
        },
        {
          "Sid": "S3ServerAccessLogsPolicy",
          "Effect": "Allow",
          "Principal": {
            "Service": "logging.s3.amazonaws.com"
          },
          "Action": [
            "s3:PutObject"
          ],
          "Resource": "${aws_s3_bucket.trail_accesslog_bucket.arn}/*",
          "Condition": {
            "ArnLike": {
              "aws:SourceArn": "${aws_s3_bucket.trail_bucket.arn}"
            },
            "StringEquals": {
              "aws:SourceAccount": "${data.aws_caller_identity.current.account_id}"
            }
          }
        }
      ]
    }
  POLICY
}


# CloudTrailバケットのアクセスログを有効化する
resource "aws_s3_bucket_logging" "trail_bucket" {
  bucket        = aws_s3_bucket.trail_bucket.id
  target_bucket = aws_s3_bucket.trail_accesslog_bucket.id # ログ送信先バケット
  target_prefix = "${aws_s3_bucket.trail_bucket.id}/"     # ログ送信先Prefix
}




#----------------------------------------
# CloudTrail出力用CloudWatchLogs
#----------------------------------------

# CloudTrailのストリーム用ロググループ
resource "aws_cloudwatch_log_group" "trail_log_group" {
  name = "${var.prefix}-trail-log-group"
  # CloudTrailはS3バケットにも格納しているため90日保存とする。
  retention_in_days = 90
}

# CloudTrailからCloudWatchLogsへの書き込みロールの信頼ポリシー
data "aws_iam_policy_document" "trail_log_group" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
  }
}


# CloudTrailからCloudWatchLogsへの書き込みロールの信頼ポリシーをアタッチ
resource "aws_iam_role" "trail_log_group" {
  name               = "${var.prefix}-trail-role"
  assume_role_policy = data.aws_iam_policy_document.trail_log_group.json
}


# CloudTrailからCloudWatchLogsへの書き込みロールのポリシー
resource "aws_iam_policy" "trail_log_group" {
  name = "${var.prefix}-trail-policy"

  policy = <<-POLICY
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          "Resource": "${aws_cloudwatch_log_group.trail_log_group.arn}:*",
          "Effect": "Allow"
        }
      ]
    }
  POLICY
}


# CloudTrailからCloudWatchLogsへの書き込みロールのポリシーをアタッチ
resource "aws_iam_role_policy_attachment" "trail_log_group" {
  role       = aws_iam_role.trail_log_group.name
  policy_arn = aws_iam_policy.trail_log_group.arn
}


#----------------------------------------
# CloudTrail
#----------------------------------------

# CloudTrail Trails証跡の有効化
resource "aws_cloudtrail" "trail" {
  name = "${var.prefix}-trail"

  # S3への出力設定
  s3_bucket_name = aws_s3_bucket.trail_bucket.id

  # SSE-KMS暗号化を有効
  kms_key_id = aws_kms_key.trail_key.arn

  # マルチリージョンの証跡
  is_multi_region_trail = true

  # グローバルサービスの証跡
  include_global_service_events = true

  # ログファイルの検証
  enable_log_file_validation = true

  # CloudWatchLogsへの出力設定
  cloud_watch_logs_group_arn = "${aws_cloudwatch_log_group.trail_log_group.arn}:*" # CloudTrail requires the Log Stream wildcard
  cloud_watch_logs_role_arn  = aws_iam_role.trail_log_group.arn

  depends_on = [
    # S3へバケットポリシーをアタッチする作業を完了してから証跡を有効化する
    # （依存関係を指定しないと初回実行時にエラーとなるため）
    aws_s3_bucket_policy.trail_bucket
  ]
}










/*

  CloudTrailで検知する異常動作をCloudWatchアラームに発報する

*/


# [CloudWatch.4] IAM ポリシーの変更に対してログ メトリック フィルターとアラームが存在することを確認する
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.4、CIS AWS Foundations Benchmark v1.4.0/4.4
# IAMポリシーの変更を検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "iam_policy_change" {
  name           = "${var.prefix}-iam-policy-change"
  pattern        = <<-PATTERN
  {
    ($.eventSource=iam.amazonaws.com) &&
    (
      ($.eventName=DeleteGroupPolicy) ||
      ($.eventName=DeleteRolePolicy) ||
      ($.eventName=DeleteUserPolicy) ||
      ($.eventName=PutGroupPolicy) ||
      ($.eventName=PutRolePolicy) ||
      ($.eventName=PutUserPolicy) ||
      ($.eventName=CreatePolicy) ||
      ($.eventName=DeletePolicy) ||
      ($.eventName=CreatePolicyVersion) ||
      ($.eventName=DeletePolicyVersion) ||
      ($.eventName=AttachRolePolicy) ||
      ($.eventName=DetachRolePolicy) ||
      ($.eventName=AttachUserPolicy) ||
      ($.eventName=DetachUserPolicy) ||
      ($.eventName=AttachGroupPolicy) ||
      ($.eventName=DetachGroupPolicy)
    )
  }
  PATTERN
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "IAMPolicyChangeEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# IAMポリシーの変更を検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "iam_policy_change" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "IAM Configuration changes detected!"
  alarm_name          = "${var.prefix}-cloudtrail-iam-policy-change"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.iam_policy_change.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.iam_policy_change.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}


# AWSアクセスキーが新規作成されたことを検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "new_accesskey_created" {
  name           = "${var.prefix}-new-accesskey-created"
  pattern        = "{($.eventName=CreateAccessKey)}"
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "NewAccessKeyCreatedEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# AWSアクセスキーが新規作成されたことを検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "new_accesskey_created" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Warning: New IAM access key was created. Please be sure this action was neccessary."
  alarm_name          = "${var.prefix}-cloudtrail-new-accesskey-created"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.new_accesskey_created.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.new_accesskey_created.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}


# rootユーザの利用を検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "root_user_policy" {
  name           = "${var.prefix}-root-user-policy"
  pattern        = <<-PATTERN
  {
    $.userIdentity.type="Root" &&
    $.userIdentity.invokedBy NOT EXISTS &&
    $.eventType !="AwsServiceEvent"
  }
  PATTERN
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "RootUserPolicyEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# rootユーザの利用を検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "root_user_policy" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Root user activity detected!"
  alarm_name          = "${var.prefix}-cloudtrail-root-user-policy"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.root_user_policy.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.root_user_policy.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}


# [CloudWatch.2] 不正な API 呼び出しに対するログ メトリック フィルターとアラームが存在することを確認する
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.1
# 権限不足を検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "unauthorized_attempts" {
  name           = "${var.prefix}-unauthorized-attempts"
  pattern        = <<-PATTERN
  {
    ($.errorCode="*UnauthorizedOperation") ||
    (($.errorCode="AccessDenied*") && ($.userIdentity.arn!="*AWSReservedSSO_ReadOnlyAccess*"))
  }
  PATTERN
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "UnauthorizedAttemptsEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# 権限不足を検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "unauthorized_attempts" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Multiple unauthorized actions or logins attempted!"
  alarm_name          = "${var.prefix}-cloudtrail-unauthorized-attempts"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.unauthorized_attempts.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.unauthorized_attempts.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "5"
  treat_missing_data  = "missing"
}


# Route53へのレコード変更を検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "change_resource_recordsets" {
  name           = "${var.prefix}-change-resource-recordsets"
  pattern        = "{($.eventName=ChangeResourceRecordSets)}"
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "ChangeResourceRecordSetsEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# Route53へのレコード変更を検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "change_resource_recordsets" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Warning: DNS record has been changed. Please be sure this action was neccessary."
  alarm_name          = "${var.prefix}-cloudtrail-change-resource-recordsets"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.change_resource_recordsets.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.change_resource_recordsets.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}


# [CloudWatch.3] MFA を使用しないマネジメントコンソールサインインに対してログメトリクスフィルターとアラームが存在することを確認します
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.2
# MFA未使用サインインを検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "mfa_unused_console_login" {
  name           = "${var.prefix}-mfa-unused-console-login"
  pattern        = <<-PATTERN
  {
    ($.eventName = "ConsoleLogin") &&
    ($.additionalEventData.MFAUsed != "Yes") &&
    ($.userIdentity.type = "IAMUser") &&
    ($.responseElements.ConsoleLogin = "Success")
  }
  PATTERN
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "MfaUnusedConsoleLoginEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# MFA未使用サインインを検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "mfa_unused_console_login" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Warning: MFA Unused ConsoleLogin."
  alarm_name          = "${var.prefix}-cloudtrail-mfa-unused-console-login"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.mfa_unused_console_login.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.mfa_unused_console_login.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}


# [CloudWatch.6] AWS Management Console 認証の失敗に対してログメトリクスフィルターとアラームが存在することを確認します
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.6、CIS AWS Foundations Benchmark v1.4.0/4.6
# マネジメントコンソールの認証失敗を検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "failed_console_login" {
  name           = "${var.prefix}-failed-console-login"
  pattern        = <<-PATTERN
  {
    ($.eventName=ConsoleLogin) &&
    ($.errorMessage="Failed authentication")
  }
  PATTERN
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "FailedConsoleLoginEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# マネジメントコンソールの認証失敗を検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "failed_console_login" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Warning: ConsoleLogin Failed authentication."
  alarm_name          = "${var.prefix}-cloudtrail-failed-console-login"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.failed_console_login.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.failed_console_login.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}


# [CloudWatch.7] カスタマーマネージドキーの無効化またはスケジュールされた削除に対するログメトリクスフィルターとアラームが存在することを確認します
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.7、CIS AWS Foundations Benchmark v1.4.0/4.7
# KMSのCMS無効化を検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "delete_kms_customerkey" {
  name           = "${var.prefix}-delete-kms-customerkey"
  pattern        = <<-PATTERN
  {
    ($.eventSource=kms.amazonaws.com) &&
    (
      ($.eventName=DisableKey) ||
      ($.eventName=ScheduleKeyDeletion)
    )
  }
  PATTERN
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "DeleteKmsCustomerkeyEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# KMSのCMS無効化を検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "delete_kms_customerkey" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Warning: KMS Customer master key was deleted. Please be sure this action was neccessary."
  alarm_name          = "${var.prefix}-cloudtrail-delete-kms-customerkey"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.delete_kms_customerkey.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.delete_kms_customerkey.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}


# [CloudWatch.8] S3 バケットポリシーの変更に対するログメトリクスフィルターとアラームが存在することを確認します
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.8、CIS AWS Foundations Benchmark v1.4.0/4.8
# バケットポリシーの変更を検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "change_bucket_policies" {
  name           = "${var.prefix}-change-bucket-policies"
  pattern        = <<-PATTERN
  {
    ($.eventSource=s3.amazonaws.com) &&
    (
      ($.eventName=PutBucketAcl) ||
      ($.eventName=PutBucketPolicy) ||
      ($.eventName=PutBucketCors) ||
      ($.eventName=PutBucketLifecycle) ||
      ($.eventName=PutBucketReplication) ||
      ($.eventName=DeleteBucketPolicy) ||
      ($.eventName=DeleteBucketCors) ||
      ($.eventName=DeleteBucketLifecycle) ||
      ($.eventName=DeleteBucketReplication)
    )
  }
  PATTERN
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "ChangeBucketPoliciesEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# バケットポリシーの変更を検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "change_bucket_policies" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Warning: S3 bucket policies was changed. Please be sure this action was neccessary."
  alarm_name          = "${var.prefix}-cloudtrail-change-bucket-policies"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.change_bucket_policies.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.change_bucket_policies.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}



# [CloudWatch.9] AWS Config 設定の変更に対してログメトリクスフィルターとアラームが存在することを確認します
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.9, CIS AWS Foundations Benchmark v1.4.0/4.9
# Configの設定変更を検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "change_config_settings" {
  name           = "${var.prefix}-change-config-settings"
  pattern        = <<-PATTERN
  {
    ($.eventSource=config.amazonaws.com) &&
    (
      ($.eventName=StopConfigurationRecorder) ||
      ($.eventName=DeleteDeliveryChannel) ||
      ($.eventName=PutDeliveryChannel) ||
      ($.eventName=PutConfigurationRecorder)
    )
  }
  PATTERN
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "ChangeConfigSettingsEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# Configの設定変更を検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "change_config_settings" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Warning: AWS Config settings was changed. Please be sure this action was neccessary."
  alarm_name          = "${var.prefix}-cloudtrail-change-config-settings"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.change_config_settings.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.change_config_settings.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}


# [CloudWatch.10] セキュリティグループの変更に対するログメトリクスフィルターとアラームが存在することを確認します
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.10、CIS AWS Foundations Benchmark v1.4.0/4.10
# event側で検知しているため、ログメトリクスフィルターとアラームは不要


# [CloudWatch.11] セキュリティグループの変更に対するログメトリクスフィルターとアラームが存在することを確認します
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.10、CIS AWS Foundations Benchmark v1.4.0/4.10
# event側で検知しているため、ログメトリクスフィルターとアラームは不要


# [CloudWatch.12] ネットワークゲートウェイへの変更に対するログメトリクスフィルターとアラームが存在することを確認します
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.12、CIS AWS Foundations Benchmark v1.4.0/4.12
# ネットワークゲートウェイの設定変更を検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "change_network_gateway" {
  name           = "${var.prefix}-change-network-gateway"
  pattern        = <<-PATTERN
  {
    ($.eventName=CreateCustomerGateway) ||
    ($.eventName=DeleteCustomerGateway) ||
    ($.eventName=AttachInternetGateway) ||
    ($.eventName=CreateInternetGateway) ||
    ($.eventName=DeleteInternetGateway) ||
    ($.eventName=DetachInternetGateway)
  }
  PATTERN
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "ChangeNetworkGatewayEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# ネットワークゲートウェイの設定変更を検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "change_network_gateway" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Warning: Network gateway was changed. Please be sure this action was neccessary."
  alarm_name          = "${var.prefix}-cloudtrail-change-network-gateway"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.change_network_gateway.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.change_network_gateway.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}


# [CloudWatch.13] ルートテーブルの変更に対してログメトリクスフィルターとアラームが存在することを確認します
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.13、CIS AWS Foundations Benchmark v1.4.0/4.13
# ルートテーブルの設定変更を検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "change_route_table" {
  name           = "${var.prefix}-change-route-table"
  pattern        = <<-PATTERN
  {
    ($.eventSource=ec2.amazonaws.com) &&
    (
      ($.eventName=CreateRoute) ||
      ($.eventName=CreateRouteTable) ||
      ($.eventName=ReplaceRoute) ||
      ($.eventName=ReplaceRouteTableAssociation) ||
      ($.eventName=DeleteRouteTable) ||
      ($.eventName=DeleteRoute) ||
      ($.eventName=DisassociateRouteTable)
    )
  }
  PATTERN
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "ChangeRouteTableEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# ルートテーブルの設定変更を検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "change_route_table" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Warning: Route table was changed. Please be sure this action was neccessary."
  alarm_name          = "${var.prefix}-cloudtrail-change-route-table"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.change_route_table.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.change_route_table.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}


# [CloudWatch.14] VPC の変更に対してログメトリクスフィルターとアラームが存在することを確認します
# Related requirements: CIS AWS Foundations Benchmark v1.2.0/3.14、CIS AWS Foundations Benchmark v1.4.0/4.14
# VPCの設定変更を検知するメトリクスフィルター
resource "aws_cloudwatch_log_metric_filter" "change_vpc_settings" {
  name           = "${var.prefix}-change-vpc-settings"
  pattern        = <<-PATTERN
  {
    ($.eventName=CreateVpc) ||
    ($.eventName=DeleteVpc) ||
    ($.eventName=ModifyVpcAttribute) ||
    ($.eventName=AcceptVpcPeeringConnection) ||
    ($.eventName=CreateVpcPeeringConnection) ||
    ($.eventName=DeleteVpcPeeringConnection) ||
    ($.eventName=RejectVpcPeeringConnection) ||
    ($.eventName=AttachClassicLinkVpc) ||
    ($.eventName=DetachClassicLinkVpc) ||
    ($.eventName=DisableVpcClassicLink) ||
    ($.eventName=EnableVpcClassicLink)
  }
  PATTERN
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  metric_transformation {
    name      = "ChangeVpcSettingsEventCount"
    namespace = "LogMetrics"
    value     = "1"
  }
}

# VPCの設定変更を検知するメトリクスアラーム
resource "aws_cloudwatch_metric_alarm" "change_vpc_settings" {
  actions_enabled     = "true"
  alarm_actions       = [var.security_sns_arn]
  alarm_description   = "Warning: VPC settings was changed. Please be sure this action was neccessary."
  alarm_name          = "${var.prefix}-cloudtrail-change-vpc-settings"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  metric_name         = aws_cloudwatch_log_metric_filter.change_vpc_settings.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.change_vpc_settings.metric_transformation[0].namespace
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  treat_missing_data  = "missing"
}
