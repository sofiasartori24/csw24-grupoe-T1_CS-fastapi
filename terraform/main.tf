# AWS Infrastructure for FastAPI Application

# Use existing RDS instance instead of creating a new one
data "aws_db_instance" "existing" {
  db_instance_identifier = "resources-management-db"
}

# Create a security group for Lambda to access RDS
resource "aws_security_group" "lambda_sg" {
  name        = "lambda-to-rds-sg-fixed"
  description = "Security group for Lambda function to access RDS"
  vpc_id      = "vpc-0f53830436b086840"  # Hardcoded VPC ID
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }
  
  tags = {
    Name        = "lambda-to-rds-sg"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
  
  # Prevent recreation of the security group
  lifecycle {
    create_before_destroy = true
    ignore_changes = [name]
  }
}

# Add a rule to the RDS security group to allow inbound connections from the Lambda security group
resource "aws_security_group_rule" "rds_ingress_from_lambda" {
  type                     = "ingress"
  from_port                = 3306
  to_port                  = 3306
  protocol                 = "tcp"
  security_group_id        = var.rds_security_group_id  # RDS security group ID
  source_security_group_id = aws_security_group.lambda_sg.id
  description              = "Allow MySQL connections from Lambda function"
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

# Create the Lambda function with a fixed name
resource "aws_lambda_function" "fastapi_lambda" {
  function_name    = "FastAPIApplication-fixed"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  role             = var.lambda_role_arn
  handler          = "lambda_handler.lambda_handler"
  runtime          = var.lambda_runtime
  memory_size      = var.lambda_memory_size
  timeout          = var.lambda_timeout
  
  # Prevent recreation of the Lambda function
  lifecycle {
    ignore_changes = [function_name]
  }

  environment {
    variables = {
      DB_HOST       = data.aws_db_instance.existing.address
      DB_USER       = var.db_username
      DB_PASSWORD   = var.db_password
      DB_NAME       = var.db_name
      DEBUG         = var.debug_mode
      LOG_LEVEL     = var.log_level
      API_VERSION   = var.api_version
      ENVIRONMENT   = var.environment
      POOL_SIZE     = var.db_pool_size
      MAX_OVERFLOW  = var.db_max_overflow
      POOL_RECYCLE  = var.db_pool_recycle
    }
  }
  
  # Add VPC configuration to allow Lambda to access RDS
  vpc_config {
    subnet_ids         = [
      "subnet-094b48a14e397a2e8",
      "subnet-0722195fdb9cc24a9",
      "subnet-0c5f6ffdd0abc5587"
    ]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }
  
  tags = {
    Name        = "FastAPIApplication"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}

# API Gateway Resources
resource "aws_apigatewayv2_api" "api_gateway" {
  name          = "fastapi-api-gateway-${var.environment}"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_headers = ["*"]
    allow_methods = ["*"]
    allow_origins = ["*"]
  }

  tags = {
    Name        = "fastapi-api-gateway-${var.environment}"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}

resource "aws_apigatewayv2_stage" "api_stage" {
  api_id      = aws_apigatewayv2_api.api_gateway.id
  name        = var.api_stage_name
  auto_deploy = true
  
  default_route_settings {
    throttling_burst_limit = var.api_throttling_burst_limit
    throttling_rate_limit  = var.api_throttling_rate_limit
    detailed_metrics_enabled = true
  }

  tags = {
    Name        = "fastapi-api-stage-${var.environment}"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
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

# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.fastapi_lambda.function_name}"
  retention_in_days = var.log_retention_days
  
  # Prevent recreation of the log group
  lifecycle {
    ignore_changes = [name]
  }

  tags = {
    Name        = "lambda-logs"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}