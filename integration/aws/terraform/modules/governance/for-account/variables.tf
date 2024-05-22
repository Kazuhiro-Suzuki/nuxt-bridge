## リソース名の共通接頭辞（例：プロジェクト名、プロジェクト名-実行環境名）
variable "prefix" {}
variable "region" {}

variable "security_sns_arn" {}

# iamモジュールで利用する変数
variable "infraadmin_sso_role_arn" {}
variable "developers_sso_role_arn" {}


# アカウント設定
## 代替連絡先
variable "account_manager_name" {}
variable "account_manager_post" {}
variable "account_manager_email" {}
variable "account_manager_phone_number" {}
