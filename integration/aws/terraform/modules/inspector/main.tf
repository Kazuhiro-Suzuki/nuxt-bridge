# 環境情報取得用データソース
data "aws_caller_identity" "current" {}

# Inspector v2の有効化
resource "aws_inspector2_enabler" "inspector" {
  account_ids    = [data.aws_caller_identity.current.account_id]
  resource_types = ["ECR"]
}


# Inspector v2 のECRスキャン時に脆弱性をSNSへ通知
# 重要度HIGH以上
resource "aws_cloudwatch_event_rule" "event_inspector" {
  description    = "CloudWatch Event Rule to send notification on new vulnerabilities."
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "detail": {
      "findings": {
        "ProductName": [ "Inspector" ],
        "RecordState": [ "ACTIVE" ],
        "Resources": {
          "Type": [ "AwsEcrContainerImage" ]
        },
        "Severity": {
          "Label": [ "HIGH",
                    "CRITICAL" ]
        }
      }
    },
    "detail-type": [ "Security Hub Findings - Imported" ],
    "source": [ "aws.securityhub" ]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-inspector"
}

resource "aws_cloudwatch_event_target" "event_inspector" {
  arn  = var.vulnerability_sns_arn
  rule = aws_cloudwatch_event_rule.event_inspector.name
}
