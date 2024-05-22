# コスト異常検知設定
resource "aws_ce_anomaly_monitor" "default" {
  name              = "${var.prefix}-anomaly-monitor"
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "SERVICE"
}

# 既定値を超えたらSNSへ通知する
resource "aws_ce_anomaly_subscription" "default" {
  name      = "${var.prefix}-anomaly-monitor"
  frequency = "IMMEDIATE"
  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_ABSOLUTE"
      values        = ["100.00"] # $100
      match_options = ["GREATER_THAN_OR_EQUAL"]
    }
  }
  monitor_arn_list = [aws_ce_anomaly_monitor.default.arn]
  subscriber {
    type    = "SNS"
    address = var.security_sns_arn
  }
}
