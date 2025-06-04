# Use existing resources instead of creating new ones
# This approach avoids issues with VPC and subnet permissions

# Use existing RDS instance instead of creating a new one
# The RDS instance already exists with identifier "resources-management-db"
data "aws_db_instance" "existing" {
  db_instance_identifier = "resources-management-db"
}

# Package the Lambda function code
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../t1_cs"
  output_path = "${path.module}/lambda_function.zip"
  
  # Exclude unnecessary files
  excludes = [
    "__pycache__",
    "*.pyc",
    ".coverage",
    ".pytest_cache"
  ]
}

# Create the Lambda function with a unique name to avoid conflicts
resource "aws_lambda_function" "fastapi_lambda" {
  function_name    = "FastAPIApplication-${formatdate("YYYYMMDDhhmmss", timestamp())}"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  role             = "arn:aws:iam::030764292549:role/LabRole"
  handler          = "lambda_handler.handler"
  runtime          = var.lambda_runtime
  memory_size      = var.lambda_memory_size
  timeout          = var.lambda_timeout

  environment {
    variables = {
      DB_HOST     = data.aws_db_instance.existing.address
      DB_USER     = var.db_username
      DB_PASSWORD = var.db_password
      DB_NAME     = var.db_name
      # Add debug environment variables
      DEBUG       = "true"
      LOG_LEVEL   = "DEBUG"
    }
  }
  
  # Removed layers due to permission issues in AWS Lab environment
}

# Use existing Lambda function instead of creating a new one
# resource "aws_lambda_function" "fastapi_lambda" {
#   function_name    = "FastAPIApplication"
#   filename         = data.archive_file.lambda_zip.output_path
#   source_code_hash = data.archive_file.lambda_zip.output_base64sha256
#   role             = "arn:aws:iam::030764292549:role/LabRole"
#   handler          = "lambda_handler.handler"
#   runtime          = "python3.9"
#   memory_size      = 512
#   timeout          = 60
#
#   environment {
#     variables = {
#       # Use environment variables for database connection
#       # since we're using an existing RDS instance
#       DB_HOST     = var.db_host
#       DB_USER     = var.db_username
#       DB_PASSWORD = var.db_password
#       DB_NAME     = var.db_name
#     }
#   }
#
#   # No dependencies on IAM resources since we're using an existing role
# }

# API Gateway Resources
resource "aws_apigatewayv2_api" "api_gateway" {
  name          = "fastapi-api-gateway"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_headers = ["*"]
    allow_methods = ["*"]
    allow_origins = ["*"]
  }
}

resource "aws_apigatewayv2_stage" "api_stage" {
  api_id      = aws_apigatewayv2_api.api_gateway.id
  name        = "Prod"
  auto_deploy = true
  
  default_route_settings {
    throttling_burst_limit = 100
    throttling_rate_limit  = 50
    detailed_metrics_enabled = true
  }
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = aws_apigatewayv2_api.api_gateway.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.fastapi_lambda.invoke_arn
  integration_method = "POST"
  payload_format_version = "1.0"
}

resource "aws_apigatewayv2_route" "proxy_route" {
  api_id    = aws_apigatewayv2_api.api_gateway.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "root_route" {
  api_id    = aws_apigatewayv2_api.api_gateway.id
  route_key = "ANY /"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.fastapi_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api_gateway.execution_arn}/*/*"
}

# Note: IAM policy attachments removed due to permission restrictions in AWS Lab environment
# The LabRole should already have the necessary permissions to access RDS