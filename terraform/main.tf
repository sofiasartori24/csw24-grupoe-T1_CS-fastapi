# Database Resources
resource "aws_db_subnet_group" "default" {
  name       = "rds-subnet-group"
  subnet_ids = var.private_subnet_ids
}

resource "aws_security_group" "rds_sg" {
  name   = "rds_sg"
  vpc_id = var.vpc_id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "lambda_sg" {
  name   = "lambda_sg"
  vpc_id = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Use existing RDS instance instead of creating a new one
# The RDS instance already exists with identifier "resources-management-db"
data "aws_db_instance" "existing" {
  db_instance_identifier = "resources-management-db"
}

# Use existing Lambda function instead of creating a new one
data "aws_lambda_function" "existing_lambda" {
  function_name = "FastAPIApplication"
}

# Keep this for reference, but don't use it to create a new Lambda
# data "archive_file" "lambda_zip" {
#   type        = "zip"
#   source_dir  = "${path.module}/../t1_cs"
#   output_path = "${path.module}/lambda_function.zip"
# }

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
}

resource "aws_apigatewayv2_stage" "api_stage" {
  api_id      = aws_apigatewayv2_api.api_gateway.id
  name        = "Prod"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = aws_apigatewayv2_api.api_gateway.id
  integration_type   = "AWS_PROXY"
  integration_uri    = data.aws_lambda_function.existing_lambda.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
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
  function_name = data.aws_lambda_function.existing_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api_gateway.execution_arn}/*/*"
}