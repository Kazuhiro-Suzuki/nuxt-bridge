# cofig-rules-main.tfでリソースを定義
output "default_security_group_closed" {
  value = aws_iam_role.default_security_group_closed
}
