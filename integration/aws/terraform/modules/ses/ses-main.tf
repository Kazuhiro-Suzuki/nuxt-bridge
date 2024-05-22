/*
SES の設定と、SES によるメール送信履歴の保存を行う。
送信履歴の保存は SES 単体では実現できないため
Kinesis Data Firehose によって S3 に記録する。
@see https://aws.amazon.com/jp/premiumsupport/knowledge-center/ses-email-sending-history/
*/

// S3
resource "aws_s3_bucket" "bucket" {
  bucket        = "${var.name}-ses"
  acl           = "private"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "bucket" {
  bucket = aws_s3_bucket.bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


// CloudWatch Logs
resource "aws_cloudwatch_log_group" "cloudwatch_log_group" {
  name = "/kinesis/firehose/${var.name}"
}

resource "aws_cloudwatch_log_stream" "cloudwatch_log_stream" {
  name           = "error"
  log_group_name = aws_cloudwatch_log_group.cloudwatch_log_group.name
}

// Kinesis
resource "aws_iam_role" "firehose-role" {
  name = "${var.name}-firehose-role"

  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "firehose.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy" "firehose-role-policy" {
  name = "${var.name}-firehose-role-policy"
  role = aws_iam_role.firehose-role.id

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Action": [
          "s3:AbortMultipartUpload",
          "s3:GetBucketLocation",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:ListBucketMultipartUploads",
          "s3:PutObject"
        ],
        "Resource": [
          "arn:aws:s3:::${aws_s3_bucket.bucket.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.bucket.bucket}/*"
        ]
      },
      {
        "Sid": "",
        "Effect": "Allow",
        "Action": [
          "logs:PutLogEvents"
        ],
        "Resource": [
          "${aws_cloudwatch_log_stream.cloudwatch_log_stream.arn}:*"
        ]
      }
    ]
  }
  EOF
}

resource "aws_kinesis_firehose_delivery_stream" "firehose" {
  name        = "${var.name}-kinesis-firehose"
  destination = "s3"

  s3_configuration {
    role_arn        = aws_iam_role.firehose-role.arn
    bucket_arn      = aws_s3_bucket.bucket.arn
    buffer_size     = 5
    buffer_interval = 60

    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = aws_cloudwatch_log_group.cloudwatch_log_group.name
      log_stream_name = aws_cloudwatch_log_stream.cloudwatch_log_stream.name
    }
  }

}

// SES
resource "aws_iam_role" "ses-role" {
  name               = "${var.name}-ses-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ses.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "ses-role-policy" {
  name = "${var.name}-ses-role-policy"
  role = aws_iam_role.ses-role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Action": [
        "firehose:PutRecord",
        "firehose:PutRecordBatch"
      ],
      "Resource": "${aws_kinesis_firehose_delivery_stream.firehose.arn}"
    }
  ]
}
EOF
}

resource "aws_ses_configuration_set" "ses" {
  name = "${var.name}-configuration-set"
}

resource "aws_ses_event_destination" "cloudwatch" {
  name                   = "${var.name}-ses-kinesis-destination"
  configuration_set_name = aws_ses_configuration_set.ses.name
  enabled                = true

  matching_types = [
    "send", "reject", "bounce", "complaint", "delivery", "open", "click", "renderingFailure"
  ]

  //  cloudwatch_destination {
  //    default_value = "dd-support-prod-configuration-set"
  //    dimension_name = "ses:configuration-set"
  //    value_source = "emailHeader"
  //  }

  kinesis_destination {
    stream_arn = aws_kinesis_firehose_delivery_stream.firehose.arn
    role_arn   = aws_iam_role.ses-role.arn
  }

  depends_on = [aws_iam_role_policy.ses-role-policy]
}
