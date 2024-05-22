#!/bin/sh
S3_NAME_FOR_TERRAFORM=milabo.lg-pwd.systemfiles
ENV=development
PROFILE=lg-pwd

aws s3 cp s3://$S3_NAME_FOR_TERRAFORM/terraform/$ENV/terraform.tfvars ./terraform.tfvars --profile $PROFILE
