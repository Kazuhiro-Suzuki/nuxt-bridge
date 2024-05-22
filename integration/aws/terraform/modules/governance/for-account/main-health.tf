# AWS Health のイベントをSNSへ通知
resource "aws_cloudwatch_event_rule" "event_aws_health" {
  description    = "Notify AWS Health event"
  event_bus_name = "default"
  event_pattern  = <<-EOF
  {
    "detail-type": [ "AWS Health Event" ],
    "source": [ "aws.health" ]
  }
  EOF
  state          = "ENABLED"
  name           = "${var.prefix}-event-aws-health"
}

resource "aws_cloudwatch_event_target" "event_aws_health" {
  arn  = var.security_sns_arn
  rule = aws_cloudwatch_event_rule.event_aws_health.name
}
