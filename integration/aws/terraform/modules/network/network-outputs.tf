output "vpc" {
  value = aws_vpc.this
}

output "public_subnets" {
  value = aws_subnet.public-subnet.*.id
}

output "private_subnets" {
  value = aws_subnet.private-subnet.*.id
}

output "security_group_lb" {
  value = aws_security_group.lb
}

output "security_group_ecs" {
  value = aws_security_group.ecs
}

output "security_group_db" {
  value = aws_security_group.db
}