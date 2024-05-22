# SecurityHub のイベントをSNSへ通知
# 重要度HIGH以上
resource "aws_cloudwatch_event_rule" "event_securityhub" {
  description    = "CloudWatch Event Rule to send notification on SecurityHub all new findings and all updates."
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "detail": {
      "findings": {
        "Compliance": {
          "Status": [ "FAILED" ]
        },
        "RecordState": [ "ACTIVE" ],
        "Severity": {
          "Label": [ "CRITICAL", "HIGH" ]
        },
        "Workflow": {
          "Status": [ "NEW", "NOTIFIED" ]
        }
      }
    },
    "detail-type": [ "Security Hub Findings - Imported" ],
    "source": [ "aws.securityhub" ]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-securityhub"
}

resource "aws_cloudwatch_event_target" "event_securityhub" {
  arn  = var.security_sns_arn
  rule = aws_cloudwatch_event_rule.event_securityhub.name
}


# ConfigRules がNON_COMPLIANTの場合にSNSへ通知
resource "aws_cloudwatch_event_rule" "event_change_configrules" {
  description    = "CloudWatch Event Rule to send notification on Config Rule compliance changes."
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "detail": {
      "newEvaluationResult": {
        "complianceType": [ "NON_COMPLIANT" ]
      }
    },
    "detail-type": [ "Config Rules Compliance Change" ],
    "source": [ "aws.config" ]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-change-configrules"
}

resource "aws_cloudwatch_event_target" "event_change_configrules" {
  arn  = var.security_sns_arn
  rule = aws_cloudwatch_event_rule.event_change_configrules.name
}


# Guard Duty のイベントをSNSへ通知
resource "aws_cloudwatch_event_rule" "event_guardduty" {
  description    = "CloudWatch Event Rule to send notification on GuardDuty findings."
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "detail": {
      "severity": [ 4,4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,
                    5,5,5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9,
                    6,6,6.1,6.2,6.3,6.4,6.5,6.6,6.7,6.8,6.9,
                    7,7,7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,7.9,
                    8,8,8.1,8.2,8.3,8.4,8.5,8.6,8.7,8.8,8.9 ]
    },
    "detail-type": [ "GuardDuty Finding" ],
    "source": [ "aws.guardduty" ]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-guardduty"
}
resource "aws_cloudwatch_event_target" "event_guardduty" {
  arn  = var.security_sns_arn
  rule = aws_cloudwatch_event_rule.event_guardduty.name
}


# Guard Duty のイベントをSNSへ通知
# Guard Dutyはリージョン集約できないため、各リージョンで検知したイベントはSecurityHubに統合された検出結果を検知する。
resource "aws_cloudwatch_event_rule" "event_guardduty_multi_region" {
  description    = "CloudWatch Event Rule to send notification on GuardDuty findings."
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "detail": {
      "findings": {
        "ProductName": [ "GuardDuty" ],
        "Severity": {
          "Label": [ "MEDIUM", "HIGH", "CRITICAL" ]
        },
        "Workflow": {
          "Status": [ "NEW" ]
        }
      }
    },
    "detail-type": [ "Security Hub Findings - Imported" ],
    "source": [ "aws.securityhub" ]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-guardduty-multi-region"
}
resource "aws_cloudwatch_event_target" "event_guardduty_multi_region" {
  arn  = var.security_sns_arn
  rule = aws_cloudwatch_event_rule.event_guardduty_multi_region.name
}


# CloudTrail の設定変更イベントをSNSへ通知
resource "aws_cloudwatch_event_rule" "event_change_cloudtrail" {
  description    = "Notify to change on CloudTrail log configuration"
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "detail":{
      "eventName": [ "StopLogging", "DeleteTrail", "UpdateTrail"],
      "eventSource": [ "cloudtrail.amazonaws.com" ]
    },
    "detail-type": [ "AWS API Call via CloudTrail" ]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-change-cloudtrail"
}

resource "aws_cloudwatch_event_target" "event_change_cloudtrail" {
  arn  = var.security_sns_arn
  rule = aws_cloudwatch_event_rule.event_change_cloudtrail.name
}


# Network ACL の設定変更イベントをSNSへ通知
resource "aws_cloudwatch_event_rule" "event_change_nacl" {
  description    = "Notify to create, update or delete a Network ACL."
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "detail": {
      "eventName": [ "CreateNetworkAcl",
                    "CreateNetworkAclEntry",
                    "DeleteNetworkAcl",
                    "DeleteNetworkAclEntry",
                    "ReplaceNetworkAclEntry",
                    "ReplaceNetworkAclAssociation" ],
      "eventSource": [ "ec2.amazonaws.com" ]
    },
    "detail-type": [ "AWS API Call via CloudTrail" ],
    "source": ["aws.ec2"]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-change-nacl"
}

resource "aws_cloudwatch_event_target" "event_change_nacl" {
  arn  = var.security_sns_arn
  rule = aws_cloudwatch_event_rule.event_change_nacl.name
}


# SecurityGroup の設定変更イベントをSNSへ通知
resource "aws_cloudwatch_event_rule" "event_change_sg" {
  description    = "Notify to create, update or delete a Security Group."
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "detail": {
      "eventName": [ "AuthorizeSecurityGroupIngress",
                    "AuthorizeSecurityGroupEgress",
                    "RevokeSecurityGroupIngress",
                    "RevokeSecurityGroupEgress" ],
      "eventSource": [ "ec2.amazonaws.com" ]
    },
    "detail-type": [ "AWS API Call via CloudTrail" ],
    "source": [ "aws.ec2" ]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-change-sg"
}

resource "aws_cloudwatch_event_target" "event_change_sg" {
  arn  = var.security_sns_arn
  rule = aws_cloudwatch_event_rule.event_change_sg.name
}


# rootユーザの利用イベントをSNSへ通知
resource "aws_cloudwatch_event_rule" "event_used_rootuser" {
  description    = "Notify to detect root user activity"
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "detail": {
      "eventType": [ { "anything-but": "AwsServiceEvent" } ],
      "userIdentity": {
        "invokedBy": [ { "exists": false } ],
        "type": [ "Root" ]
      }
    },
    "detail-type": [ "AWS API Call via CloudTrail" ]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-used-rootuser"
}

resource "aws_cloudwatch_event_target" "event_used_rootuser" {
  arn  = var.security_sns_arn
  rule = aws_cloudwatch_event_rule.event_used_rootuser.name
}


# SSM Session Manager のセッション開始をSNSへ通知
resource "aws_cloudwatch_event_rule" "event_start_ssm" {
  description    = "Notify to Session Manager Start"
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "detail": {
      "eventName": [ "StartSession" ],
      "eventSource": [ "ssm.amazonaws.com" ]
    },
    "detail-type": [ "AWS API Call via CloudTrail" ],
    "source": [ "aws.ssm" ]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-start-ssm"
}
resource "aws_cloudwatch_event_target" "event_start_ssm" {
  arn  = var.security_sns_arn
  rule = aws_cloudwatch_event_rule.event_start_ssm.name
}


# CodePipelineの利用イベントをSNSへ通知
resource "aws_cloudwatch_event_rule" "event_codepipeline" {
  description    = "This rule is used to route CodeBuild, CodeCommit, CodeDeploy, CodePipeline, and other Code Suite notifications to CodeStar Notifications"
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "source": [ "aws.codebuild",
                "aws.codecommit",
                "aws.codedeploy",
                "aws.codepipeline" ]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-codepipeline"
}

resource "aws_cloudwatch_event_target" "event_codepipeline" {
  arn  = var.security_sns_arn
  rule = aws_cloudwatch_event_rule.event_codepipeline.name
}
