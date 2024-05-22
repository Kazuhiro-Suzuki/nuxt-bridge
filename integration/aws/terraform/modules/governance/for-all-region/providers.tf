# 各リージョンに対してリソースを作成する際に必要になるプロバイダー設定
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}
