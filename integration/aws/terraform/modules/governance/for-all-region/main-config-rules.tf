/*
  aws_config_configuration_recorderはOrganizationsで有効化済みのため、
  rulesリソース作成時の depends_onは不要
*/


/*
  Subnet作成時に、デフォルトで作成されるSecurityGroupのAllAllowルールを
  自動的に削除するためSSMオートメーションと連携する。
*/

# Config Rules
resource "aws_config_config_rule" "default_security_group_closed" {
  description = "Checks that the default security group of any Amazon Virtual Private Cloud (VPC) does not allow inbound or outbound traffic. The rule is non-compliant if the default security group has one or more inbound or outbound traffic."

  name = "customer-rule-${var.prefix}-check-for-default-sg-closed"

  scope {
    compliance_resource_types = ["AWS::EC2::SecurityGroup"]
  }

  source {
    owner             = "AWS"
    source_identifier = "VPC_DEFAULT_SECURITY_GROUP_CLOSED"
  }
}

# SSM Automation Document
resource "aws_config_remediation_configuration" "default_security_group_closed" {
  # SSM Automation が利用できないリージョンがあるためフラグで作成を制御する
  #   2023/7/7時点でap-northeast-3リージョンに利用予定のオートメーションドキュメントが提供されていない（デフォルトSGの削除は手動で実施する）
  count            = var.default_security_group_closed_automation ? 1 : 0
  config_rule_name = aws_config_config_rule.default_security_group_closed.name

  target_type    = "SSM_DOCUMENT"
  target_id      = "AWSConfigRemediation-RemoveVPCDefaultSecurityGroupRules"
  target_version = "1"

  parameter {
    name         = "AutomationAssumeRole"
    static_value = var.default_security_group_closed_role_arn
  }
  parameter {
    name           = "GroupId"
    resource_value = "RESOURCE_ID"
  }

  automatic                  = true
  maximum_automatic_attempts = 5
  retry_attempt_seconds      = 60

}
