/*
  すべてのリージョンに対して適用する設定
    - EBSデフォルト暗号化を全てのリージョンで有効化する
    - デフォルトSecurityGroupのインバウンド・アウトバウンドルールの削除自動化のためのConfigRules
*/


module "governance_for_all_region_us_east_1" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.us-east-1
  }
}

module "governance_for_all_region_us_east_2" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.us-east-2
  }
}

module "governance_for_all_region_us_west_1" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.us-west-1
  }
}

module "governance_for_all_region_us_west_2" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.us-west-2
  }
}

module "governance_for_all_region_ap_south_1" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.ap-south-1
  }
}

module "governance_for_all_region_ap_northeast_1" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.ap-northeast-1
  }
}

module "governance_for_all_region_ap_northeast_2" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.ap-northeast-2
  }
}

module "governance_for_all_region_ap_northeast_3" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = false # AutomationDocumentが無いため無効化
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.ap-northeast-3
  }
}

module "governance_for_all_region_ap_southeast_1" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.ap-southeast-1
  }
}

module "governance_for_all_region_ap_southeast_2" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.ap-southeast-2
  }
}

module "governance_for_all_region_ca_central_1" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.ca-central-1
  }
}

module "governance_for_all_region_eu_central_1" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.eu-central-1
  }
}

module "governance_for_all_region_eu_west_1" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.eu-west-1
  }
}

module "governance_for_all_region_eu_west_2" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.eu-west-2
  }
}

module "governance_for_all_region_eu_west_3" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.eu-west-3
  }
}

module "governance_for_all_region_eu_north_1" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.eu-north-1
  }
}

module "governance_for_all_region_sa_east_1" {
  source                                   = "../../modules/governance/for-all-region"
  prefix                                   = var.prefix
  default_security_group_closed_automation = true
  default_security_group_closed_role_arn   = module.governance_for_account.default_security_group_closed.arn
  providers = {
    aws = aws.sa-east-1
  }
}
