# AWS Infrastructure for FastAPI Application

# Get existing VPC information
data "aws_vpc" "selected" {
  id = var.vpc_id
}

# Get subnet information
data "aws_subnet" "selected" {
  count = length(var.private_subnet_ids)
  id    = var.private_subnet_ids[count.index]
}

# Create a DB subnet group for RDS
resource "aws_db_subnet_group" "rds_subnet_group" {
  name        = "resources-management-subnet-group"
  description = "Subnet group for RDS instance"
  subnet_ids  = var.private_subnet_ids

  tags = {
    Name        = "resources-management-subnet-group"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}

# Create a security group for RDS
resource "aws_security_group" "rds_sg" {
  name        = "resources-management-rds-sg"
  description = "Security group for RDS instance"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]
    description     = "Allow MySQL connections from Lambda function"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name        = "resources-management-rds-sg"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}

# Create a security group for Lambda to access RDS
resource "aws_security_group" "lambda_sg" {
  name        = "lambda-to-rds-sg"
  description = "Security group for Lambda function to access RDS"
  vpc_id      = var.vpc_id
  
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
}

# Create RDS MySQL instance
resource "aws_db_instance" "rds" {
  identifier             = "resources-management-db"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = var.db_instance_class
  allocated_storage      = var.db_allocated_storage
  storage_type           = "gp2"
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  parameter_group_name   = "default.mysql8.0"
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot    = true
  publicly_accessible    = false
  multi_az               = var.db_multi_az
  backup_retention_period = var.db_backup_retention_period
  deletion_protection    = var.db_deletion_protection

  tags = {
    Name        = "resources-management-db"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
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

# Create IAM role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "lambda-execution-role"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}

# Attach policies to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_vpc" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

# Create the Lambda function
resource "aws_lambda_function" "fastapi_lambda" {
  function_name    = "FastAPIApplication-${var.environment}"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_handler.lambda_handler"
  runtime          = var.lambda_runtime
  memory_size      = var.lambda_memory_size
  timeout          = var.lambda_timeout

  environment {
    variables = {
      DB_HOST       = aws_db_instance.rds.address
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
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda_sg.id]
  }
  
  tags = {
    Name        = "FastAPIApplication-${var.environment}"
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

  tags = {
    Name        = "lambda-logs-${var.environment}"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}