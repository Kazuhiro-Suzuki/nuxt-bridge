variable "name" {}
variable "security_group" {}
variable "public_subnets" {}
variable "access_log_bucket" {}
variable "access_log_enabled" {}
variable "vpc" {}
variable "acm_arn" {}

variable "route53_zone_id" {}
variable "white_ip_addresses_for_admin" {}
//variable "frontend_resident_domain" {}
//variable "frontend_region_staff_domain" {}
variable "frontend_domain" {}
variable "cdn" {}
variable "backend_domain" {}
variable "temp_url_domain" {}
variable "cdn_for_temp_url" {}
