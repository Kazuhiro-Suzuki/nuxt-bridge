# 未使用の証明書のため廃止
# output "cert" {
#   value = aws_acm_certificate.cert
# }

output "cert_for_backend" {
  value = aws_acm_certificate.cert_for_backend
}

output "cert_for_cloudfront" {
  value = var.create_cert_for_cloudfront ? aws_acm_certificate.cert_for_cloudfront[0] : null
}

output "cert_for_cloudfront_temp_url" {
  value = aws_acm_certificate.cert_for_cloudfront_temp_url
}
