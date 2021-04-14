resource "aws_lambda_function" "func" {
  filename      = var.function_filename
  function_name = var.service_name
  role          = aws_iam_role.iam_for_lambda.arn
  runtime       = var.runtime
  handler = "lambda_handler.lambda_handler"
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.func.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.this.arn
}
