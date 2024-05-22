resource "aws_s3_bucket" "front" {
  bucket = var.frontend_bucket
  acl    = "private"
}

# # バージョンアップに伴い定義が変更されたため
# resource "aws_s3_bucket_acl" "front" {
#   bucket = aws_s3_bucket.front.id
#   acl    = "private"
# }

resource "aws_s3_bucket_public_access_block" "front" {
  bucket                  = aws_s3_bucket.front.bucket
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_cloudfront_origin_access_identity" "front" {
  comment = var.frontend_bucket
}

data "aws_iam_policy_document" "front" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]

    resources = [
      aws_s3_bucket.front.arn,
      "${aws_s3_bucket.front.arn}/*",
    ]

    principals {
      type = "AWS"
      identifiers = [
        aws_cloudfront_origin_access_identity.front.iam_arn
      ]
    }
  }
}

// Lambda@Edge
data "aws_iam_policy_document" "lambda-edge-policy-document" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["edgelambda.amazonaws.com", "lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy" "lambda-basic-execution-policy" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy_document" "maintenance-policy-document" {
  source_json = data.aws_iam_policy.lambda-basic-execution-policy.policy

  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "maintenance-policy" {
  name   = "${var.name}-maintenance-lambda-edge-policy"
  policy = data.aws_iam_policy_document.maintenance-policy-document.json
}

resource "aws_iam_role" "maintenance-role" {
  name = "${var.name}-maintenance-lambda-edge-role"

  assume_role_policy = data.aws_iam_policy_document.lambda-edge-policy-document.json
}

resource "aws_iam_role_policy_attachment" "maintenance-role-policy-attachment" {
  role       = aws_iam_role.maintenance-role.name
  policy_arn = aws_iam_policy.maintenance-policy.arn
}

data "template_file" "maintenance-template-file" {
  template = file("../../modules/frontend/lambda/maintenance/lambda_function.py")

  vars = {
    white_ip_addresses = var.white_ip_addresses
  }
}

data "archive_file" "maintenance-archive-file" {
  type        = "zip"
  output_path = "lambda/dist/maintenance.zip"

  source {
    content  = data.template_file.maintenance-template-file.rendered
    filename = "lambda_function.py"
  }
}

resource "aws_lambda_function" "maintenance" {
  provider         = aws.cloudfront_region
  filename         = data.archive_file.maintenance-archive-file.output_path
  function_name    = "${var.name}-maintenance"
  role             = aws_iam_role.maintenance-role.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.maintenance-archive-file.output_base64sha256
  runtime          = "python3.8"

  publish = true

  memory_size = 128
  timeout     = 5
}

resource "aws_s3_bucket_policy" "front" {
  bucket = aws_s3_bucket.front.id
  policy = data.aws_iam_policy_document.front.json
}

resource "aws_cloudfront_distribution" "this" {
  enabled = true
  aliases = [
    //    var.frontend_resident_domain,
    //    var.frontend_region_staff_domain,
    var.frontend_domain
  ]
  comment             = var.frontend_domain
  default_root_object = "index.html"
  is_ipv6_enabled     = true
  origin {
    origin_id   = aws_s3_bucket.front.id
    domain_name = aws_s3_bucket.front.bucket_regional_domain_name
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.front.cloudfront_access_identity_path
    }
  }
  origin {
    origin_id   = var.backend_domain
    domain_name = var.backend_domain
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }
  restrictions {
    geo_restriction {
      locations        = []
      restriction_type = "none"
    }
  }
  viewer_certificate {
    acm_certificate_arn      = var.acm_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2019"
  }
  default_cache_behavior {
    target_origin_id = aws_s3_bucket.front.id
    allowed_methods = [
      "DELETE",
      "GET",
      "HEAD",
      "OPTIONS",
      "PATCH",
      "POST",
      "PUT"
    ]
    cached_methods = [
      "GET",
      "HEAD"
    ]
    viewer_protocol_policy = "redirect-to-https"
    forwarded_values {
      query_string            = true
      query_string_cache_keys = []
      cookies {
        forward = "none"
      }
    }
    compress    = true
    min_ttl     = 0
    default_ttl = 86400
    max_ttl     = 2592000

    # lambda_function_association {
    #     event_type = "viewer-request"
    #     lambda_arn = aws_lambda_function.maintenance.qualified_arn
    # }
  }
  ordered_cache_behavior {
    target_origin_id = var.backend_domain
    allowed_methods = [
      "DELETE",
      "GET",
      "HEAD",
      "OPTIONS",
      "PATCH",
      "POST",
      "PUT"
    ]
    cached_methods = [
      "GET",
      "HEAD"
    ]
    path_pattern           = "/api/*"
    viewer_protocol_policy = "redirect-to-https"
    forwarded_values {
      query_string            = true
      query_string_cache_keys = []
      cookies {
        forward = "all"
      }
      headers = [
        "Authorization",
        "X-Forwarded-For",
        "User-Agent",
        "Host"
      ]
    }
    min_ttl     = 0
    default_ttl = 0
    max_ttl     = 0
  }
  custom_error_response {
    error_caching_min_ttl = 0
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
  }
  custom_error_response {
    error_caching_min_ttl = 0
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
  }
  logging_config {
    include_cookies = false
    bucket          = var.log_bucket
    prefix          = "logs/${var.frontend_bucket}"
  }
}




#----------------------------------------
# 一時公開用エンドポイント用
#----------------------------------------

# 静的サイト用S3
resource "aws_s3_bucket" "temp_url" {
  bucket = "${var.name}-${var.env}-temp-url"
  # 検証時などで強制削除したい場合は、trueを設定
  force_destroy = false
}

# アクセス制御ブロック
resource "aws_s3_bucket_public_access_block" "temp_url" {
  bucket = aws_s3_bucket.temp_url.bucket
  # パブリックアクセスはしないため全て有効にする
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


resource "aws_cloudfront_origin_access_identity" "temp_url" {
  comment = aws_s3_bucket.temp_url.bucket
}


# IAMポリシー
data "aws_iam_policy_document" "temp_url" {
  # S3に以下の権限を付与
  # ・オブジェクト取得
  # ・オブジェクト一覧表示
  statement {
    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]

    resources = [
      "${aws_s3_bucket.temp_url.arn}",
      "${aws_s3_bucket.temp_url.arn}/*",
    ]

    principals {
      type = "AWS"
      identifiers = [
        "${aws_cloudfront_origin_access_identity.temp_url.iam_arn}"
      ]
    }
  }

  # s3-bucket-ssl-requests-only準拠のため、暗号化されている通信のみを許可する
  statement {
    sid    = "AllowSSLRequestsOnly"
    effect = "Deny"
    actions = [
      "s3:*",
    ]
    resources = [
      "${aws_s3_bucket.temp_url.arn}",
      "${aws_s3_bucket.temp_url.arn}/*",
    ]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "temp_url" {
  bucket = aws_s3_bucket.temp_url.id
  policy = data.aws_iam_policy_document.temp_url.json
}



# CloudFront
data "aws_cloudfront_cache_policy" "caching_disabled" {
  name = "Managed-CachingDisabled"
}


resource "aws_cloudfront_distribution" "temp_url" {
  enabled = true
  # CNAME
  aliases             = [var.temp_url_domain]
  comment             = var.temp_url_domain
  default_root_object = "index.html"
  is_ipv6_enabled     = true

  # frontendの配信元
  origin {
    origin_id   = aws_s3_bucket.temp_url.id
    domain_name = aws_s3_bucket.temp_url.bucket_regional_domain_name
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.temp_url.cloudfront_access_identity_path
    }
  }
  origin {
    origin_id   = var.backend_domain
    domain_name = var.backend_domain
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }
  # 配信地域設定
  restrictions {
    geo_restriction {
      locations        = []
      restriction_type = "none"
    }
  }

  # SSL証明書設定
  viewer_certificate {
    acm_certificate_arn      = var.temp_url_acm_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  # frontend用キャッシュ設定
  default_cache_behavior {
    target_origin_id = aws_s3_bucket.temp_url.id
    allowed_methods = [
      "DELETE",
      "GET",
      "HEAD",
      "OPTIONS",
      "PATCH",
      "POST",
      "PUT"
    ]
    cached_methods = [
      "GET",
      "HEAD"
    ]

    # HTTPS通信のみ許可
    viewer_protocol_policy = "redirect-to-https"

    cache_policy_id = data.aws_cloudfront_cache_policy.caching_disabled.id
    # origin_request_policy_id = data.aws_cloudfront_origin_request_policy.allviewer.id
  }

  ordered_cache_behavior {
    target_origin_id = var.backend_domain
    allowed_methods = [
      "DELETE",
      "GET",
      "HEAD",
      "OPTIONS",
      "PATCH",
      "POST",
      "PUT"
    ]
    cached_methods = [
      "GET",
      "HEAD"
    ]
    path_pattern           = "/htp-api/*"
    viewer_protocol_policy = "redirect-to-https"
    forwarded_values {
      query_string            = true
      query_string_cache_keys = []
      cookies {
        forward = "all"
      }
      headers = [
        "Authorization",
        "X-Forwarded-For",
        "User-Agent",
        "Host"
      ]
    }
    min_ttl     = 0
    default_ttl = 0
    max_ttl     = 0
  }

  # アクセスログ設定
  logging_config {
    bucket          = var.log_bucket
    prefix          = "logs/${var.temp_url_domain}/"
    include_cookies = false
  }

  web_acl_id = var.temp_url_waf_arn
}
