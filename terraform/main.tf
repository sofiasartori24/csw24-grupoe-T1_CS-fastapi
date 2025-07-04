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

# Build Docker image for Lambda
resource "null_resource" "docker_build" {
  # Force rebuild on every apply to ensure latest code is deployed
  triggers = {
    always_run = "${timestamp()}"
    handler_hash = filemd5("${path.module}/../t1_cs/simple_lambda_handler.py")
    main_hash = filemd5("${path.module}/../t1_cs/app/main.py")
  }

  provisioner "local-exec" {
    command = <<EOF
      cd ${path.module}/..
      docker build -t fastapi-lambda:latest -f Dockerfile.lambda .
      docker tag fastapi-lambda:latest ${var.ecr_repository_url}:latest
      aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${var.ecr_repository_url}
      docker push ${var.ecr_repository_url}:latest
    EOF
  }
}

# Create the Lambda function with a fixed name using Docker image
resource "aws_lambda_function" "fastapi_lambda" {
  function_name    = "FastAPIApplication-20250605005207"
  image_uri        = "${var.ecr_repository_url}:latest"
  package_type     = "Image"
  role             = var.lambda_role_arn
  memory_size      = var.lambda_memory_size
  timeout          = var.lambda_timeout
  
  depends_on       = [null_resource.docker_build]

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
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"]
    allow_origins = ["*"]
    allow_credentials = false
    expose_headers = ["Content-Type", "X-Requested-With", "Authorization"]
    max_age = 86400
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
  payload_format_version = "2.0"  # Changed to 2.0 for better compatibility with Mangum
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
  name              = "/aws/lambda/FastAPIApplication-20250605005207"
  retention_in_days = var.log_retention_days

  tags = {
    Name        = "lambda-logs"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}