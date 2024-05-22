####################
# S3
####################
resource "aws_s3_bucket" "alb_logs_bucket" {
  acl    = "private"
  bucket = var.access_log_bucket

  # S3バケットのデフォルト暗号化
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

}

resource "aws_s3_bucket_public_access_block" "alb_logs_bucket" {
  bucket = aws_s3_bucket.alb_logs_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 東京リージョン（ap-northeast-1）の
# Elastic Load Balancing アカウント ID（582318560864）
data "aws_elb_service_account" "main" {}

# S3 Bucket Policy
data "aws_iam_policy_document" "alb_logs_iam_policy_document" {
  statement {
    effect    = "Allow"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.alb_logs_bucket.arn}/*"]
    principals {
      type        = "AWS"
      identifiers = [data.aws_elb_service_account.main.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "alb_logs_bucket_policy" {
  bucket = aws_s3_bucket.alb_logs_bucket.id
  policy = data.aws_iam_policy_document.alb_logs_iam_policy_document.json
}



####################
# ALB
####################
resource "aws_alb" "public" {
  name = "${var.name}-alb"
  security_groups = [
    var.security_group.id
  ]
  subnets                    = var.public_subnets
  internal                   = false
  enable_deletion_protection = true
  drop_invalid_header_fields = true

  access_logs {
    bucket  = aws_s3_bucket.alb_logs_bucket.bucket
    enabled = var.access_log_enabled
  }
}

resource "aws_alb_target_group" "api" {
  name        = "${var.name}-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc.id
  health_check {
    path = "/api/health-check/"
  }
}

# resource "aws_alb_listener" "alb_80" {
#   load_balancer_arn = aws_alb.public.arn
#   port              = "80"
#   protocol          = "HTTP"

#   default_action {
#     type = "redirect"
#     redirect {
#       protocol    = "HTTPS"
#       port        = "443"
#       status_code = "HTTP_301"
#     }
#   }
# }

resource "aws_alb_listener" "alb_443" {
  load_balancer_arn = aws_alb.public.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.acm_arn

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "401 Unauthorized"
      status_code  = "401"
    }
  }
}

resource "aws_lb_listener_rule" "api" {

  listener_arn = aws_alb_listener.alb_443.arn
  priority     = 10

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.api.arn
  }

  condition {
    host_header {
      values = [var.frontend_domain]
    }
  }

  condition {
    path_pattern {
      values = ["/api/*"]
    }
  }
}

# アプリ経由のアクセスを許可する（アプリ側のURLを修正後にこの設定は削除すること）
resource "aws_lb_listener_rule" "api_mobile" {

  listener_arn = aws_alb_listener.alb_443.arn
  priority     = 11

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.api.arn
  }

  condition {
    host_header {
      values = [var.backend_domain]
    }
  }

  condition {
    path_pattern {
      values = ["/api/*"]
    }
  }
}
# アプリ経由のアクセスを許可する（アプリ側のURLを修正後にこの設定は削除すること）


resource "aws_lb_listener_rule" "htp_api" {

  listener_arn = aws_alb_listener.alb_443.arn
  priority     = 20

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.api.arn
  }

  condition {
    host_header {
      values = [var.temp_url_domain]
    }
  }

  condition {
    path_pattern {
      values = ["/htp-api/*"]
    }
  }
}

# Django管理画面
resource "aws_lb_listener_rule" "forward_admin_console" {
  listener_arn = aws_alb_listener.alb_443.arn
  priority     = 90

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.api.arn
  }

  condition {
    host_header {
      values = [var.backend_domain]
    }
  }

  condition {
    path_pattern {
      values = ["/admin/*", "/static/*", ]
    }
  }

  condition {
    source_ip {
      values = var.white_ip_addresses_for_admin # 特定IPのみ許可する
    }
  }
}



####################
# DNS設定
####################
resource "aws_route53_record" "frontend" {
  zone_id = var.route53_zone_id
  name    = var.frontend_domain
  type    = "A"
  alias {
    name                   = var.cdn.domain_name
    zone_id                = var.cdn.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "backend" {
  zone_id = var.route53_zone_id
  name    = var.backend_domain
  type    = "A"
  alias {
    name                   = aws_alb.public.dns_name
    zone_id                = aws_alb.public.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "temp_url" {
  zone_id = var.route53_zone_id
  name    = var.temp_url_domain
  type    = "A"
  alias {
    name                   = var.cdn_for_temp_url.domain_name
    zone_id                = var.cdn_for_temp_url.hosted_zone_id
    evaluate_target_health = false
  }
}
