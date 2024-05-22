/*

  リージョン集約してアラートを飛ばすサービス群
  メインリージョンでのみ有効化する。

*/

# セキュリティ関連の通知用チャンネル
module "chatbot_security_channel" {
  source = "../../modules/chatbot"

  prefix             = var.prefix
  slack_workspace_id = var.slack_workspace_id
  slack_channel_id   = var.slack_channel_id_security
  notification_type  = var.notification_type_security
}


# コンテナイメージの脆弱性関連の通知用チャンネル
module "chatbot_vulnerability_channel" {
  source = "../../modules/chatbot"

  prefix             = var.prefix
  slack_workspace_id = var.slack_workspace_id
  slack_channel_id   = var.slack_channel_id_vulnerability
  notification_type  = var.notification_type_vulnerability
}

/*

  AWSアカウント共通の設定

*/

module "governance_for_account" {
  source = "../../modules/governance/for-account"

  prefix                       = var.prefix
  region                       = var.region
  security_sns_arn             = module.chatbot_security_channel.sns_topic_chatbot.arn
  infraadmin_sso_role_arn      = var.infraadmin_sso_role_arn
  developers_sso_role_arn      = var.developers_sso_role_arn
  account_manager_name         = var.account_manager_name
  account_manager_post         = var.account_manager_post
  account_manager_email        = var.account_manager_email
  account_manager_phone_number = var.account_manager_phone_number
}

module "inspector" {
  source = "../../modules/inspector"

  prefix                = var.prefix
  vulnerability_sns_arn = module.chatbot_vulnerability_channel.sns_topic_chatbot.arn
}
