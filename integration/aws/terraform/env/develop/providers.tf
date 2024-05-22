terraform {
  required_version = "1.4.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.76.1"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4.1"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.4.3"
    }
    template = {
      source  = "hashicorp/template"
      version = "~> 2.2.0"
    }
  }
  backend "s3" {
    bucket  = "milabo.lg-pwd.systemfiles"
    key     = "terraform/development/terraform.tfstate"
    region  = "ap-northeast-1"
    profile = "lg-pwd"
  }
}

# var.* は develop/terraform.tfvars に定義する

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      ResourceGroup = var.name
      ResourceEnv   = var.env
    }
  }
  profile = var.aws_profile
}


provider "aws" {
  region = "us-east-1"
  alias  = "us-east-1"
  default_tags {
    tags = {
      ResourceGroup = var.name
      ResourceEnv   = var.env
    }
  }
  profile = var.aws_profile
}
