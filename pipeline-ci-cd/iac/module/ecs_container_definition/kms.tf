resource "aws_kms_key" "kms_key_cloudwatch" {
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  description              = "KMS key to encrypt/decrypt ${var.app_name} CloudWatch log group."
  enable_key_rotation      = true
  is_enabled               = true
  key_usage                = "ENCRYPT_DECRYPT"
  multi_region             = false

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Action   = "kms:*"
        Effect   = "Allow"
        Resource = "*"

        Principal = {
          AWS = data.aws_caller_identity.current.account_id
        }
      },
      {
        Effect   = "Allow"
        Resource = "*"

        Action = [
          "kms:Decrypt*",
          "kms:Describe*",
          "kms:Encrypt*",
          "kms:GenerateDataKey*",
          "kms:ReEncrypt*",
        ]

        Condition = {
          ArnEquals = {
            "kms:EncryptionContext:aws:logs:arn" = "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:${local.cloudwatch_group}"
          }
        }

        Principal = {
          Service = "logs.${var.region}.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_kms_alias" "kms_alias_cloudwatch" {
  name          = "alias/${var.workspace}/cloudwatch/logs${local.cloudwatch_group}"
  target_key_id = aws_kms_key.kms_key_cloudwatch.key_id
}