# /*

#   SecurityHub（CIS AWS Foundations Benchmark v1.2.0）準拠のIAMパスワードポリシーを設定する
#     https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/iam-controls.html#iam-11
#     https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/iam-controls.html#iam-12
#     https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/iam-controls.html#iam-13
#     https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/iam-controls.html#iam-14
#     https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/iam-controls.html#iam-15
#     https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/iam-controls.html#iam-16
#     https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/iam-controls.html#iam-17

# */


# resource "aws_iam_account_password_policy" "account_password_policy" {
#   require_uppercase_characters   = true # [IAM.11]
#   require_lowercase_characters   = true # [IAM.12]
#   require_symbols                = true # [IAM.13]
#   require_numbers                = true # [IAM.14]
#   minimum_password_length        = 14   # [IAM.15]
#   password_reuse_prevention      = 24   # [IAM.16]
#   max_password_age               = 90   # [IAM.17]
#   allow_users_to_change_password = true
# }










# /*

#   AWSアカウントの作業用SSOユーザがスイッチするIAMロール

# */


# # プロダクトのインフラ管理者用ロールを設定（milaboInfraAdminAccessRole）
# resource "aws_iam_role" "milabo_infraadmin_access_role" {
#   name               = "milaboInfraAdminAccessRole"
#   assume_role_policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": {
#         "AWS": "${var.infraadmin_sso_role_arn}"
#       },
#       "Action": "sts:AssumeRole"
#     }
#   ]
# }
# EOF
# }

# # プロダクトのインフラ管理者用ロールへアタッチするポリシーを定義
# # プロダクト毎に要件にあったIAMポリシーを定義すること
# resource "aws_iam_role_policy" "milabo_infraadmin_access_role" {
#   name = "milabo_infraadmin_access_role_policy"
#   role = aws_iam_role.milabo_infraadmin_access_role.id

#   policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#       {
#         "Sid": "ManagementConsoleLoginHome",
#         "Action": [
#           "ce:GetCostAndUsage",
#           "ce:GetCostForecast",
#           "health:DescribeEventAggregates",
#           "notifications:ListNotificationHubs",
#           "ram:ListResources",
#           "securityhub:DescribeHub",
#           "securityhub:GetAdministratorAccount",
#           "securityhub:GetControlFindingSummary",
#           "securityhub:GetFindingAggregator",
#           "securityhub:GetInsightResults",
#           "securityhub:ListFindingAggregators",
#           "securityhub:ListMembers",
#           "servicecatalog:ListApplications",
#           "support:DescribeTrustedAdvisorChecks",
#           "support:DescribeTrustedAdvisorCheckSummaries"
#         ],
#         "Resource": "*",
#         "Effect": "Allow"
#       },
#       {
#         "Sid": "CloudWatchLogsReadOnly",
#         "Effect": "Allow",
#         "Action": [
#           "oam:ListSinks",
#           "cloudwatch:DescribeInsightRules",
#           "cloudwatch:DescribeAlarmsForMetric",
#           "cloudwatch:GetMetricData",
#           "notifications:ListNotificationHubs",
#           "health:DescribeEventAggregates",
#           "resource-groups:ListGroups",
#           "cloudwatch:DescribeAlarms",
#           "cloudwatch:GetDashboard"
#         ],
#         "Resource": "*"
#       },
#       {
#         "Sid": "TerraformApply",
#         "Effect": "Allow",
#         "Action": [
#           "apigateway:*",
#           "cloudformation:*",
#           "cloudfront:*",
#           "cloudwatch:*",
#           "ec2:*",
#           "ecs:*",
#           "elasticache:*",
#           "elasticloadbalancing:*",
#           "events:*",
#           "firehose:*",
#           "iam:*",
#           "kms:*",
#           "lambda:*",
#           "rds:*",
#           "route53:*",
#           "s3:*",
#           "secretsmanager:*",
#           "ses:*",
#           "SNS:*",
#           "ssm:*",
#           "wafv2:*",
#           "config:*",
#           "logs:*",
#           "inspector2:*",
#           "chatbot:*",
#           "cloudtrail:*",
#           "application-autoscaling:*"
#         ],
#         "Resource": "*"
#       }
#   ]
# }
# EOF
# }

# # プロダクトのインフラ管理者用ロールへAWSマネージドポリシー（WellArchitectedConsoleFullAccess）をアタッチ
# resource "aws_iam_role_policy_attachment" "milabo_infraadmin_access_manage_policy_attachment_wellarchited" {
#   role       = aws_iam_role.milabo_infraadmin_access_role.name
#   policy_arn = "arn:aws:iam::aws:policy/WellArchitectedConsoleFullAccess"
# }

# # プロダクトのインフラ管理者用ロールへAWSマネージドポリシー（AWSSupportAccess）をアタッチ
# resource "aws_iam_role_policy_attachment" "milabo_infraadmin_access_manage_policy_attachment_support" {
#   role       = aws_iam_role.milabo_infraadmin_access_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AWSSupportAccess"
# }





# # プロダクトのアプリケーション開発者用ロールを設定（milaboDevelopersAccessRole）
# resource "aws_iam_role" "milabo_developers_access_role" {
#   name               = "milaboDevelopersAccessRole"
#   assume_role_policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": {
#         "AWS": "${var.developers_sso_role_arn}"
#       },
#       "Action": "sts:AssumeRole"
#     }
#   ]
# }
# EOF
# }

# # プロダクトのアプリケーション開発者用ロールへアタッチするポリシーを定義
# # プロダクト毎に要件にあったIAMポリシーを定義すること
# resource "aws_iam_role_policy" "milabo_developers_access_role" {
#   name = "milabo_developers_access_role_policy"
#   role = aws_iam_role.milabo_developers_access_role.id

#   policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#       {
#         "Sid": "ManagementConsoleLoginHome",
#         "Action": [
#           "ce:GetCostAndUsage",
#           "ce:GetCostForecast",
#           "health:DescribeEventAggregates",
#           "notifications:ListNotificationHubs",
#           "ram:ListResources",
#           "securityhub:DescribeHub",
#           "securityhub:GetAdministratorAccount",
#           "securityhub:GetControlFindingSummary",
#           "securityhub:GetFindingAggregator",
#           "securityhub:GetInsightResults",
#           "securityhub:ListFindingAggregators",
#           "securityhub:ListMembers",
#           "servicecatalog:ListApplications",
#           "support:DescribeTrustedAdvisorChecks",
#           "support:DescribeTrustedAdvisorCheckSummaries"
#         ],
#         "Resource": "*",
#         "Effect": "Allow"
#       },
#       {
#         "Sid": "CloudWatchLogsReadOnly",
#         "Effect": "Allow",
#         "Action": [
#           "oam:ListSinks",
#           "cloudwatch:DescribeInsightRules",
#           "cloudwatch:DescribeAlarmsForMetric",
#           "cloudwatch:GetMetricData",
#           "notifications:ListNotificationHubs",
#           "health:DescribeEventAggregates",
#           "resource-groups:ListGroups",
#           "cloudwatch:DescribeAlarms",
#           "cloudwatch:GetDashboard"
#         ],
#         "Resource": "*"
#       }
#   ]
# }
# EOF
# }

# # プロダクトのアプリケーション開発者用ロールへAWSマネージドポリシー（CloudWatchLogsReadOnlyAccess）をアタッチ
# resource "aws_iam_role_policy_attachment" "milabo_developers_access_manage_policy_attachment_cloudwacthlogs" {
#   role       = aws_iam_role.milabo_developers_access_role.name
#   policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsReadOnlyAccess"
# }

# # プロダクトのアプリケーション開発者用ロールへAWSマネージドポリシー（WellArchitectedConsoleFullAccess）をアタッチ
# resource "aws_iam_role_policy_attachment" "milabo_developers_access_manage_policy_attachment_wellarchited" {
#   role       = aws_iam_role.milabo_developers_access_role.name
#   policy_arn = "arn:aws:iam::aws:policy/WellArchitectedConsoleFullAccess"
# }

# # プロダクトのアプリケーション開発者用ロールへAWSマネージドポリシー（AWSSupportAccess）をアタッチ
# resource "aws_iam_role_policy_attachment" "milabo_developers_access_manage_policy_attachment_support" {
#   role       = aws_iam_role.milabo_developers_access_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AWSSupportAccess"
# }
