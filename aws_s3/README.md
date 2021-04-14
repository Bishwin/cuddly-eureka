# aws s3 lambda parser

## About
Providers resources to provision an S3 bucket that invokes a Lambda on object PUT

## Getting Started

In project code define and import as example shows below
```
provider "aws" {
  region = "eu-west-2"
}

module "coffeedracula" {
  source       = "../../aws_s3" # path to module src or registry
  service_name = "coffee-count-dracula" # name of app
  function_filename = "../app/lambda_handler.zip" # path of code zip
}
```

### Variables
| name | type | default |
|---|---|--|
| service_name| `string` | required |
| function_file | `string` | required |
| runtime | `string` | "python3.8" |