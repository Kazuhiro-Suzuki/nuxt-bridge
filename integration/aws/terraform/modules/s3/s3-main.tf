resource "aws_kms_key" "encrypt_key" {
  description             = "This key is used to encrypt bucket objects"
  deletion_window_in_days = 10
}
resource "aws_kms_alias" "encrypt_key" {
  name          = "alias/${var.name}-kms-key-for-bucket"
  target_key_id = aws_kms_key.encrypt_key.key_id
}


resource "aws_iam_role" "replication" {
  name = "${var.name}-iam-role-for-s3-replication"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
POLICY
}

resource "aws_iam_policy" "replication" {
  name = "${var.name}-iam-role-policy-for-replication"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:GetReplicationConfiguration",
        "s3:ListBucket"
      ],
      "Effect": "Allow",
      "Resource": [
        "${aws_s3_bucket.source.arn}"
      ]
    },
    {
      "Action": [
        "s3:GetObjectVersionForReplication",
        "s3:GetObjectVersionAcl",
        "s3:GetObjectVersionTagging"
      ],
      "Effect": "Allow",
      "Resource": [
        "${aws_s3_bucket.source.arn}/*"
      ]
    },
    {
      "Action": [
        "s3:ReplicateObject",
        "s3:ReplicateDelete",
        "s3:ReplicateTags"
      ],
      "Effect": "Allow",
      "Resource": "${aws_s3_bucket.destination.arn}/*"
    },
    {
       "Action":[
          "kms:Decrypt"
       ],
       "Effect":"Allow",
       "Condition":{
          "StringLike":{
             "kms:ViaService":"s3.${aws_s3_bucket.source.region}.amazonaws.com",
             "kms:EncryptionContext:aws:s3:arn":[
                "${aws_s3_bucket.source.arn}/*"
             ]
          }
       },
       "Resource":[
         "${aws_kms_key.encrypt_key.arn}"
       ]
      },
      {
         "Action":[
            "kms:Encrypt"
         ],
         "Effect":"Allow",
         "Condition":{
            "StringLike":{
               "kms:ViaService":"s3.${aws_s3_bucket.destination.region}.amazonaws.com",
               "kms:EncryptionContext:aws:s3:arn":[
                  "${aws_s3_bucket.destination.arn}/*"
               ]
            }
         },
         "Resource":[
            "${aws_kms_key.encrypt_key.arn}"
         ]
      }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "replication" {
  role       = aws_iam_role.replication.name
  policy_arn = aws_iam_policy.replication.arn
}

resource "aws_s3_bucket" "destination" {
  bucket = "${var.name}-backup"
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = aws_kms_key.encrypt_key.arn
        sse_algorithm     = "aws:kms"
      }
    }
  }
  logging {
    target_bucket = "lg-pwd-s3-server-access-log"
    target_prefix = "${var.name}-backup/"
  }
}

resource "aws_s3_bucket" "source" {
  bucket = var.name
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = aws_kms_key.encrypt_key.arn
        sse_algorithm     = "aws:kms"
      }
    }
  }

  replication_configuration {
    role = aws_iam_role.replication.arn

    rules {
      id     = "${var.name}-backup"
      status = "Enabled"

      destination {
        bucket        = aws_s3_bucket.destination.arn
        storage_class = "STANDARD"

        replica_kms_key_id = aws_kms_key.encrypt_key.arn
      }

      source_selection_criteria {
        sse_kms_encrypted_objects {
          enabled = true
        }
      }
    }
  }
  logging {
    target_bucket = "lg-pwd-s3-server-access-log"
    target_prefix = "${var.name}/"
  }
}

resource "aws_s3_bucket_public_access_block" "source-bucket-access-block" {
  bucket                  = aws_s3_bucket.source.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "destination-bucket-access-block" {
  bucket                  = aws_s3_bucket.destination.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_object" "screening-test-folder" {
  key        = "screening-tests/"
  bucket     = aws_s3_bucket.source.id
  kms_key_id = aws_kms_key.encrypt_key.arn
}

resource "aws_s3_bucket_object" "screening-answer-folder" {
  key        = "screening-answers/"
  bucket     = aws_s3_bucket.source.id
  kms_key_id = aws_kms_key.encrypt_key.arn
}
