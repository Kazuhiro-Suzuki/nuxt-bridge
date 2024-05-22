#----------------------------------------
# 代替連絡先設定
#----------------------------------------

# 請求に関する連絡先
resource "aws_account_alternate_contact" "billing" {
  alternate_contact_type = "BILLING"
  name                   = var.account_manager_name
  title                  = var.account_manager_post
  email_address          = var.account_manager_email
  phone_number           = var.account_manager_phone_number
}

# オペレーションに関する連絡先
resource "aws_account_alternate_contact" "operations" {
  alternate_contact_type = "OPERATIONS"
  name                   = var.account_manager_name
  title                  = var.account_manager_post
  email_address          = var.account_manager_email
  phone_number           = var.account_manager_phone_number
}

# セキュリティに関する連絡先
resource "aws_account_alternate_contact" "security" {
  alternate_contact_type = "SECURITY"
  name                   = var.account_manager_name
  title                  = var.account_manager_post
  email_address          = var.account_manager_email
  phone_number           = var.account_manager_phone_number
}
