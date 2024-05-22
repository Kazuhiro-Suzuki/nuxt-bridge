#!/bin/sh
S3_NAME_FOR_TERRAFORM=milabo.lg-pwd.systemfiles
ENV=staging
PROFILE=lg-pwd

aws s3 cp ./terraform.tfvars s3://$S3_NAME_FOR_TERRAFORM/terraform/$ENV/terraform.tfvars --profile $PROFILE
