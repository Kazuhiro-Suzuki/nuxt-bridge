# Chatbotのロール
data "aws_iam_policy_document" "chatbot_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["chatbot.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "chatbot" {
  name               = "${var.prefix}-${var.notification_type}-chatbot-role"
  assume_role_policy = data.aws_iam_policy_document.chatbot_assume_role.json
}


# ChatbotのロールにCloudWatchReadOnlyAccessをアタッチ
resource "aws_iam_role_policy_attachment" "chatbot" {
  role       = aws_iam_role.chatbot.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess"
}

# SNS Topic
resource "aws_sns_topic" "chatbot" {
  name = "${var.prefix}-${var.notification_type}-chatbot-topic"
}

# Chatbot
# terraformリソースが実装されていないためCloudFormationで代替する。
resource "aws_cloudformation_stack" "chatbot" {
  name = "${var.prefix}-${var.notification_type}-chatbot-stack"

  template_body = yamlencode({
    Description = "Managed by Terraform"
    Resources = {
      AlertNotifications = {
        Type = "AWS::Chatbot::SlackChannelConfiguration"
        Properties = {
          ConfigurationName = "${var.prefix}-${var.notification_type}-chatbot-slackchannel"
          SlackWorkspaceId  = var.slack_workspace_id
          SlackChannelId    = var.slack_channel_id
          LoggingLevel      = "INFO"
          IamRoleArn        = aws_iam_role.chatbot.arn
          SnsTopicArns      = [aws_sns_topic.chatbot.arn]
        }
      }
    }
  })
}
