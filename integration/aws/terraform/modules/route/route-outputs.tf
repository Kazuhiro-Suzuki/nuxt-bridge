output "alb" {
  value = aws_alb.public
}

output "target_group" {
  value = aws_alb_target_group.api
}