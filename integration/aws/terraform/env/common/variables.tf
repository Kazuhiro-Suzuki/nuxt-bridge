###########################
# 全モジュール共通
###########################

## リソース名の共通接頭辞（例：プロジェクト名、プロジェクト名-実行環境名）
variable "prefix" {}
variable "region" {}


##########################
# chatbotモジュール
##########################
variable "slack_workspace_id" {}
variable "slack_channel_id_security" {}
variable "notification_type_security" {}
variable "slack_channel_id_vulnerability" {}
variable "notification_type_vulnerability" {}


##########################
# governanceモジュール
##########################
variable "infraadmin_sso_role_arn" {}
variable "developers_sso_role_arn" {}
variable "account_manager_name" {}
variable "account_manager_post" {}
variable "account_manager_email" {}
variable "account_manager_phone_number" {}
