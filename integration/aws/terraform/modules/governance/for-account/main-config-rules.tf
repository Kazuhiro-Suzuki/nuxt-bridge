
/*
  ConfigRulesはBLEAを踏襲
    https://github.com/aws-samples/baseline-environment-on-aws/blob/main/usecases/blea-gov-base-standalone/cfn/AWS-Control-Tower-Detective-Guardrails.yaml
  aws_config_configuration_recorderはOrganizationsで有効化済みのため、rulesリソース作成時の depends_onは不要
*/


# Amazon EBS 最適化が有効性をチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/ebs-optimized-instance.html
resource "aws_config_config_rule" "check_for_ebs_optimized_instance" {
  description = "Disallow launch of EC2 instance types that are not EBS-optimized - Checks whether EBS optimization is enabled for your EC2 instances that can be EBS-optimized"
  name        = "customer-rule-${var.prefix}-check-for-ebs-optimized-instance"

  scope {
    compliance_resource_types = ["AWS::EC2::Instance"]
  }

  source {
    owner             = "AWS"
    source_identifier = "EBS_OPTIMIZED_INSTANCE"
  }
}


# インスタンスの削除時に EBS ボリュームが削除対象としてマークされるかをチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/ec2-volume-inuse-check.html
resource "aws_config_config_rule" "check_for_ec2_volume_in_us" {
  description      = "Disallow EBS volumes that are unattached to an EC2 instance - Checks whether EBS volumes are attached to EC2 instances"
  input_parameters = "{\"deleteOnTermination\":\"true\"}"
  name             = "customer-rule-${var.prefix}-check-for-ec2-volumes-in-us"

  scope {
    compliance_resource_types = ["AWS::EC2::Volume"]
  }

  source {
    owner             = "AWS"
    source_identifier = "EC2_VOLUME_INUSE_CHECK"
  }
}


# EBS ボリュームが暗号化されているかをチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/encrypted-volumes.html
resource "aws_config_config_rule" "check_for_encrypted_volumes" {
  description = "Enable encryption for EBS volumes attached to EC2 instances - Checks whether EBS volumes that are in an attached state are encrypted."
  name        = "customer-rule-${var.prefix}-check-for-encrypted-volumes"

  scope {
    compliance_resource_types = ["AWS::EC2::Volume"]
  }

  source {
    owner             = "AWS"
    source_identifier = "ENCRYPTED_VOLUMES"
  }
}


# IAMユーザーのMFA設定をチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/mfa-enabled-for-iam-console-access.html
resource "aws_config_config_rule" "check_for_iam_console_mfa" {
  description                 = "Disallow console access to IAM users without MFA - Checks whether AWS Multi-Factor Authentication (MFA) is enabled for all AWS Identity and Access Management (IAM) users that use a console password. The rule is COMPLIANT if MFA is enabled."
  maximum_execution_frequency = "One_Hour"
  name                        = "customer-rule-${var.prefix}-check-for-iam-user-console-mfa"

  source {
    owner             = "AWS"
    source_identifier = "MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"
  }
}


# IAMユーザーのMFA設定をチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/iam-user-mfa-enabled.html
resource "aws_config_config_rule" "check_for_iam_user_mfa" {
  description                 = "Disallow access to IAM users without MFA - Checks whether the AWS Identity and Access Management users have multi-factor authentication (MFA) enabled. The rule is COMPLIANT if MFA is enabled."
  maximum_execution_frequency = "One_Hour"
  name                        = "customer-rule-${var.prefix}-check-for-iam-user-mfa"

  source {
    owner             = "AWS"
    source_identifier = "IAM_USER_MFA_ENABLED"
  }
}


# RDSスナップショットがパブリックアクセスをチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/rds-snapshots-public-prohibited.html
resource "aws_config_config_rule" "check_for_public_rds_snapshots" {
  description = "Disallow public access to RDS database snapshots - Checks if Amazon Relational Database Service (Amazon RDS) snapshots are public. The rule is non-compliant if any existing and new Amazon RDS snapshots are public."
  name        = "customer-rule-${var.prefix}-check-for-public-rds-snapshots"

  scope {
    compliance_resource_types = ["AWS::RDS::DBSnapshot"]
  }

  source {
    owner             = "AWS"
    source_identifier = "RDS_SNAPSHOTS_PUBLIC_PROHIBITED"
  }
}


# RDSのパブリックアクセス設定をチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/rds-instance-public-access-check.html
resource "aws_config_config_rule" "check_for_rds_public_access" {
  description = "Disallow public access to RDS database instances - Checks whether the Amazon Relational Database Service (RDS) instances are not publicly accessible. The rule is non-compliant if the publiclyAccessible field is true in the instance configuration item."
  name        = "customer-rule-${var.prefix}-check-for-rds-public-access"

  scope {
    compliance_resource_types = ["AWS::RDS::DBInstance"]
  }

  source {
    owner             = "AWS"
    source_identifier = "RDS_INSTANCE_PUBLIC_ACCESS_CHECK"
  }
}


# RDSストレージの暗号化の有効性をチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/rds-storage-encrypted.html
resource "aws_config_config_rule" "check_for_rds_storage_encryption" {
  description = "Disallow RDS database instances that are not storage encrypted - Checks whether storage encryption is enabled for your RDS DB instances."
  name        = "customer-rule-${var.prefix}-check-for-rds-storage-encryption"

  scope {
    compliance_resource_types = ["AWS::RDS::DBInstance"]
  }

  source {
    owner             = "AWS"
    source_identifier = "RDS_STORAGE_ENCRYPTED"
  }
}


# SecurityGroupの指定ポートの許可をチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/restricted-common-ports.html
resource "aws_config_config_rule" "check_for_restricted_common_ports_policy" {
  description      = "Disallow internet connection through RDP - Checks whether security groups that are in use disallow unrestricted incoming TCP traffic to the specified ports."
  input_parameters = <<-INPUT
  {
    "blockedPort1": "20",
    "blockedPort2": "21",
    "blockedPort3": "3389",
    "blockedPort4": "3306",
    "blockedPort5": "4333"
  }
  INPUT
  name             = "customer-rule-${var.prefix}-check-for-restricted-common-ports-policy"

  scope {
    compliance_resource_types = ["AWS::EC2::SecurityGroup"]
  }

  source {
    owner             = "AWS"
    source_identifier = "RESTRICTED_INCOMING_TRAFFIC"
  }
}


# SecurityGroupのSSHポートの許可をチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/restricted-ssh.html
resource "aws_config_config_rule" "check_for_restricted_ssh_policy" {
  description = "Disallow internet connection through SSH - Checks whether security groups that are in use disallow unrestricted incoming SSH traffic."
  name        = "customer-rule-${var.prefix}-check-for-restricted-ssh-policy"

  scope {
    compliance_resource_types = ["AWS::EC2::SecurityGroup"]
  }

  source {
    owner             = "AWS"
    source_identifier = "INCOMING_SSH_DISABLED"
  }
}


# ルートユーザーが多要素認証の有効性をチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/root-account-mfa-enabled.html
resource "aws_config_config_rule" "check_for_root_mfa" {
  description                 = "Enable MFA for the root user - Checks whether the root user of your AWS account requires multi-factor authentication for console sign-in."
  maximum_execution_frequency = "One_Hour"
  name                        = "customer-rule-${var.prefix}-check-for-root-mfa"

  source {
    owner             = "AWS"
    source_identifier = "ROOT_ACCOUNT_MFA_ENABLED"
  }
}


# S3バケットのパブリック読み取りアクセスの有効性をチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/s3-bucket-public-read-prohibited.html
resource "aws_config_config_rule" "check_for_s3_public_read" {
  description = "Disallow public read access to S3 buckets - Checks that your S3 buckets do not allow public read access. If an S3 bucket policy or bucket ACL allows public read access, the bucket is noncompliant."
  name        = "customer-rule-${var.prefix}-check-for-s3-public-read"

  scope {
    compliance_resource_types = ["AWS::S3::Bucket"]
  }

  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_PUBLIC_READ_PROHIBITED"
  }
}


# S3バケットのパブリック書き込みアクセスの有効性をチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/s3-bucket-public-write-prohibited.html
resource "aws_config_config_rule" "check_for_s3_public_write" {
  description = "Disallow public write access to S3 buckets - Checks that your S3 buckets do not allow public write access. If an S3 bucket policy or bucket ACL allows public write access, the bucket is noncompliant."
  name        = "customer-rule-${var.prefix}-check-for-s3-public-write"

  scope {
    compliance_resource_types = ["AWS::S3::Bucket"]
  }

  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_PUBLIC_WRITE_PROHIBITED"
  }
}

# S3バケットのバージョニングの有効性をチェックするConfigルール
# https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/s3-bucket-versioning-enabled.html
resource "aws_config_config_rule" "check_for_s3_versioning_enabled" {
  description = "Disallow S3 buckets that are not versioning enabled - Checks whether versioning is enabled for your S3 buckets."

  name = "customer-rule-${var.prefix}-check-for-s3-versioning-enabled"

  scope {
    compliance_resource_types = ["AWS::S3::Bucket"]
  }

  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_VERSIONING_ENABLED"
  }
}







# SSM Automation用のロール（default_security_group_closed）
# 各リージョンで共通のものを利用するためマルチリージョン向けモジュールではなくこちらに定義
data "aws_iam_policy_document" "default_security_group_closed" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ssm.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "default_security_group_closed" {
  name               = "config-rule-${var.prefix}-default-sg-closed-ssm-role"
  assume_role_policy = data.aws_iam_policy_document.default_security_group_closed.json
}

resource "aws_iam_policy" "default_security_group_closed" {
  name = "config-rule-${var.prefix}-default-sg-closed-ssm-policy"

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "ec2:DescribeSecurityGroups",
          "ec2:RevokeSecurityGroupEgress",
          "ec2:RevokeSecurityGroupIngress"
        ],
        "Effect": "Allow",
        "Resource": "*"
      },
      {
        "Action": "iam:PassRole",
        "Effect": "Allow",
        "Resource": "${aws_iam_role.default_security_group_closed.arn}"
      },
      {
        "Action": "ssm:StartAutomationExecution",
        "Effect": "Allow",
        "Resource": "arn:aws:ssm:::automation-definition/AWSConfigRemediation-RemoveVPCDefaultSecurityGroupRules"
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy_attachment" "default_security_group_closed" {
  role       = aws_iam_role.default_security_group_closed.name
  policy_arn = aws_iam_policy.default_security_group_closed.arn
}

