resource "aws_cloudwatch_metric_alarm" "ecs" {
  count               = length(var.ecs_alarms)
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]
  alarm_name          = var.ecs_alarms[count.index]["alarm_name"]
  comparison_operator = var.ecs_alarms[count.index]["comparison_operator"]
  evaluation_periods  = var.ecs_alarms[count.index]["evaluation_periods"]
  threshold           = var.ecs_alarms[count.index]["threshold"]
  metric_name         = var.ecs_alarms[count.index]["metric_name"]
  namespace           = var.ecs_alarms[count.index]["namespace"]
  period              = var.ecs_alarms[count.index]["period"]
  statistic           = var.ecs_alarms[count.index]["statistic"]
  alarm_description   = var.ecs_alarms[count.index]["alarm_description"]
  dimensions          = var.ecs_alarms[count.index]["dimensions"]
}

resource "aws_cloudwatch_metric_alarm" "rds" {
  count               = length(var.rds_alarms)
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]
  alarm_name          = var.rds_alarms[count.index]["alarm_name"]
  comparison_operator = var.rds_alarms[count.index]["comparison_operator"]
  evaluation_periods  = var.rds_alarms[count.index]["evaluation_periods"]
  threshold           = var.rds_alarms[count.index]["threshold"]
  metric_name         = var.rds_alarms[count.index]["metric_name"]
  namespace           = var.rds_alarms[count.index]["namespace"]
  period              = var.rds_alarms[count.index]["period"]
  statistic           = var.rds_alarms[count.index]["statistic"]
  alarm_description   = var.rds_alarms[count.index]["alarm_description"]
}

resource "aws_cloudwatch_metric_alarm" "alb" {
  count               = length(var.alb_alarms)
  alarm_actions       = [var.sns_arn]
  ok_actions          = [var.sns_arn]
  alarm_name          = var.alb_alarms[count.index]["alarm_name"]
  comparison_operator = var.alb_alarms[count.index]["comparison_operator"]
  evaluation_periods  = var.alb_alarms[count.index]["evaluation_periods"]
  threshold           = var.alb_alarms[count.index]["threshold"]
  metric_name         = var.alb_alarms[count.index]["metric_name"]
  namespace           = var.alb_alarms[count.index]["namespace"]
  period              = var.alb_alarms[count.index]["period"]
  statistic           = var.alb_alarms[count.index]["statistic"]
  alarm_description   = var.alb_alarms[count.index]["alarm_description"]
}
