provider "aws" {
  region = "eu-west-2"
}

module "coffeedracula" {
  source       = "../../aws_s3"
  service_name = "coffee-count-dracula"
  function_filename = "../app/lambda_handler.zip"
}
