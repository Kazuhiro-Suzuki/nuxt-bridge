# 未使用の証明書のため廃止
# resource "aws_acm_certificate" "cert" {
#   domain_name       = var.domain_name
#   validation_method = "DNS"
# }

resource "aws_acm_certificate" "cert_for_cloudfront" {
  count             = var.create_cert_for_cloudfront ? 1 : 0
  provider          = aws.cloudfront_region
  domain_name       = var.domain_name
  validation_method = "DNS"
}

resource "aws_acm_certificate" "cert_for_backend" {
  validation_method = "DNS"
  domain_name       = var.backend_domain
}

resource "aws_route53_record" "cert_validation" {
  provider = aws.cloudfront_region
  for_each = {
    for domain_validation_option in var.create_cert_route53_record ? aws_acm_certificate.cert_for_cloudfront[0].domain_validation_options : [] : domain_validation_option.domain_name => {
      # for domain_validation_option in var.create_cert_route53_record ? aws_acm_certificate.cert.domain_validation_options : [] : domain_validation_option.domain_name => {
      name   = domain_validation_option.resource_record_name
      record = domain_validation_option.resource_record_value
      type   = domain_validation_option.resource_record_type
    }
  }

  zone_id = var.route53_zone_id
  name    = each.value.name
  records = [each.value.record]
  type    = each.value.type
  ttl     = 60
}

resource "aws_route53_record" "cert_validation_for_backend" {
  for_each = {
    for domain_validation_option in var.create_cert_route53_record ? aws_acm_certificate.cert_for_backend.domain_validation_options : [] : domain_validation_option.domain_name => {
      name   = domain_validation_option.resource_record_name
      record = domain_validation_option.resource_record_value
      type   = domain_validation_option.resource_record_type
    }
  }

  zone_id = var.route53_zone_id
  name    = each.value.name
  records = [each.value.record]
  type    = each.value.type
  ttl     = 60
}

# 未使用の証明書のため廃止
# resource "aws_acm_certificate_validation" "cert" {
#   certificate_arn         = aws_acm_certificate.cert.arn
#   validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
# }

resource "aws_acm_certificate_validation" "cert_for_cloudfront" {
  provider                = aws.cloudfront_region
  certificate_arn         = aws_acm_certificate.cert_for_cloudfront[0].arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}

resource "aws_acm_certificate_validation" "cert_for_backend" {
  certificate_arn         = aws_acm_certificate.cert_for_backend.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation_for_backend : record.fqdn]
}



#----------------------------------------
# 一時公開用エンドポイント用
#----------------------------------------

resource "aws_acm_certificate" "cert_for_cloudfront_temp_url" {
  provider          = aws.cloudfront_region
  domain_name       = var.temp_url_domain
  validation_method = "DNS"
}


resource "aws_route53_record" "cert_validation_for_cloudfront_temp_url" {
  provider = aws.cloudfront_region
  for_each = {
    for domain_validation_option in var.create_cert_route53_record ? aws_acm_certificate.cert_for_cloudfront_temp_url.domain_validation_options : [] : domain_validation_option.domain_name => {
      name   = domain_validation_option.resource_record_name
      record = domain_validation_option.resource_record_value
      type   = domain_validation_option.resource_record_type
    }
  }
  zone_id = var.route53_zone_id
  name    = each.value.name
  records = [each.value.record]
  type    = each.value.type
  ttl     = 60
}


resource "aws_acm_certificate_validation" "cert_for_cloudfront_temp_url" {
  provider                = aws.cloudfront_region
  certificate_arn         = aws_acm_certificate.cert_for_cloudfront_temp_url.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation_for_cloudfront_temp_url : record.fqdn]
}
