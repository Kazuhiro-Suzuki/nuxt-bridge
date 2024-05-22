#----------------------------------------
# terraformの環境設定(バージョン固定化、tfstateファイルの保存先指定)
#----------------------------------------
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.36.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4.0"
    }
  }

  # TODO: 事前にS3バケットを作成しておく
  backend "s3" {
    bucket  = "milabo.lg-pwd.systemfiles"
    key     = "terraform/common/terraform.tfstate"
    region  = "ap-northeast-1"
    profile = "lg-pwd"
  }
}

#----------------------------------------
# プロバイダーの設定
#----------------------------------------

# 共通利用するローカル変数を定義
locals {
  # TODO: AWSのプロファイル設定をし、そのプロファイル名を指定する
  profile = "lg-pwd"
}

# メインリージョンの設定
provider "aws" {
  region  = var.region
  profile = local.profile
}

# 全てのリージョン操作するためのproviderを設定

# 以下のリージョンは有効化しない限り管理対象にする必要はない
# af-south-1 アフリカ (ケープタウン)
# ap-east-1 アジアパシフィック (香港)
# eu-south-1 欧州 (ミラノ)
# me-south-1 中東 (バーレーン)
# See also https://docs.aws.amazon.com/general/latest/gr/rande-manage.html
# また、providerを動的に処理することができない（2023/7/7時点の仕様）ため可読性が低いが各リージョンごとの設定を列記する。
provider "aws" {
  region  = "us-east-1"
  alias   = "us-east-1"
  profile = local.profile
}

provider "aws" {
  region  = "us-east-2"
  alias   = "us-east-2"
  profile = local.profile
}

provider "aws" {
  region  = "us-west-1"
  alias   = "us-west-1"
  profile = local.profile
}

provider "aws" {
  region  = "us-west-2"
  alias   = "us-west-2"
  profile = local.profile
}

provider "aws" {
  region  = "ap-south-1"
  alias   = "ap-south-1"
  profile = local.profile
}

provider "aws" {
  region  = "ap-northeast-1"
  alias   = "ap-northeast-1"
  profile = local.profile
}

provider "aws" {
  region  = "ap-northeast-2"
  alias   = "ap-northeast-2"
  profile = local.profile
}

provider "aws" {
  region  = "ap-northeast-3"
  alias   = "ap-northeast-3"
  profile = local.profile
}

provider "aws" {
  region  = "ap-southeast-1"
  alias   = "ap-southeast-1"
  profile = local.profile
}

provider "aws" {
  region  = "ap-southeast-2"
  alias   = "ap-southeast-2"
  profile = local.profile
}

provider "aws" {
  region  = "ca-central-1"
  alias   = "ca-central-1"
  profile = local.profile
}

provider "aws" {
  region  = "eu-central-1"
  alias   = "eu-central-1"
  profile = local.profile
}

provider "aws" {
  region  = "eu-west-1"
  alias   = "eu-west-1"
  profile = local.profile
}

provider "aws" {
  region  = "eu-west-2"
  alias   = "eu-west-2"
  profile = local.profile
}

provider "aws" {
  region  = "eu-west-3"
  alias   = "eu-west-3"
  profile = local.profile
}

provider "aws" {
  region  = "eu-north-1"
  alias   = "eu-north-1"
  profile = local.profile
}

provider "aws" {
  region  = "sa-east-1"
  alias   = "sa-east-1"
  profile = local.profile
}
