resource "aws_cloudwatch_log_group" "log_group" {
  name              = local.cloudwatch_group
  kms_key_id        = aws_kms_key.kms_key_cloudwatch.arn
  retention_in_days = 14

  depends_on = [
    aws_kms_key.kms_key_cloudwatch,
    aws_kms_alias.kms_alias_cloudwatch
  ]
}