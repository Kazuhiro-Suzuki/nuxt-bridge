# EBSのデフォルトの暗号化を有効化
resource "aws_ebs_encryption_by_default" "this" {
  enabled = true
}
