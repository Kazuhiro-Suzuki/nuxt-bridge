/*

  IP Set

*/

# 許可されるIPアドレスのリスト
resource "aws_wafv2_ip_set" "allowed_ip_set" {
  name               = "${var.prefix}-allowed-ip-set"
  scope              = "CLOUDFRONT"
  ip_address_version = "IPV4"
  addresses          = var.allowed_ip_list
}



/*

  CloudWatch Log

*/

resource "aws_cloudwatch_log_group" "this" {
  # aws-waf-logsから始まる必要がある
  name              = "aws-waf-logs-${var.prefix}"
  retention_in_days = 7
}



/*

  Web ACL

*/

# https://zenn.dev/bun913/articles/waf-cloudfront-by-terraform
# https://github.com/bun913/aws_cloudfront_and_waf/blob/main/infra/production/modules/web_app/waf.tf
resource "aws_wafv2_web_acl" "this" {
  name        = "${var.prefix}-web-acl"
  description = "Web ACL for ${var.prefix}"
  scope       = "CLOUDFRONT"

  default_action {
    allow {}
  }

  rule {
    name     = "allowed-ip-rule"
    priority = 1
    action {
      block {}
    }
    statement {
      not_statement {
        statement {
          ip_set_reference_statement {
            arn = aws_wafv2_ip_set.allowed_ip_set.arn
          }
        }
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "${var.prefix}-allowed-ip-rule-metric"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "${var.prefix}-web-acl-metric"
    sampled_requests_enabled   = true
  }
}



/*

  Web ACLのログ設定

*/

resource "aws_wafv2_web_acl_logging_configuration" "this" {
  log_destination_configs = [aws_cloudwatch_log_group.this.arn]
  resource_arn            = aws_wafv2_web_acl.this.arn

  logging_filter {
    default_behavior = "KEEP"
    filter {
      behavior = "DROP"
      condition {
        action_condition {
          action = "ALLOW"
        }
      }
      requirement = "MEETS_ANY"
    }
  }
}

