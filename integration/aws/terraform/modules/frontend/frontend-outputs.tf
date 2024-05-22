output "cdn" {
  value = aws_cloudfront_distribution.this
}

output "cdn_for_temp_url" {
  value = aws_cloudfront_distribution.temp_url
}
