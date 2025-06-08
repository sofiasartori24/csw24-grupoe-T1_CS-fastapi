variable "vpc_id" {
  description = "ID of the VPC where RDS and Lambda will run"
  type        = string
}

variable "private_subnet_ids" {
  description = "List of IDs of the private subnets where RDS and Lambda will run"
  type        = list(string)
}

variable "db_name" {
  description = "Name of the MySQL database"
  type        = string
  default     = "resources_management"
}

variable "db_username" {
  description = "MySQL username"
  type        = string
  default     = "user"
}

variable "db_password" {
  description = "MySQL user password"
  type        = string
  default     = "password"
  sensitive   = true
}

variable "rds_security_group_id" {
  description = "ID of the security group for the RDS instance"
  type        = string
  default     = "sg-087e6b149c05647f2"  # Default from previous configuration
}

variable "lambda_role_arn" {
  description = "ARN of the IAM role for the Lambda function"
  type        = string
  default     = "arn:aws:iam::030764292549:role/LabRole"  # Default from previous configuration
}

variable "db_pool_size" {
  description = "Size of the database connection pool"
  type        = string
  default     = "5"
}

variable "db_max_overflow" {
  description = "Maximum overflow connections for the database connection pool"
  type        = string
  default     = "10"
}

variable "db_pool_recycle" {
  description = "Connection recycle time in seconds"
  type        = string
  default     = "300"
}

variable "lambda_memory_size" {
  description = "Memory size for the Lambda function in MB"
  type        = number
  default     = 512
}

variable "lambda_timeout" {
  description = "Timeout for the Lambda function in seconds"
  type        = number
  default     = 60
}

variable "lambda_runtime" {
  description = "Runtime for the Lambda function"
  type        = string
  default     = "python3.9"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "resources-management"
}

variable "debug_mode" {
  description = "Whether to enable debug mode"
  type        = string
  default     = "true"
}

variable "log_level" {
  description = "Log level for the application"
  type        = string
  default     = "DEBUG"
}

variable "api_version" {
  description = "Version of the API"
  type        = string
  default     = "1.0.0"
}

variable "api_stage_name" {
  description = "Name of the API Gateway stage"
  type        = string
  default     = "Prod"
}

variable "api_throttling_burst_limit" {
  description = "API Gateway throttling burst limit"
  type        = number
  default     = 100
}

variable "api_throttling_rate_limit" {
  description = "API Gateway throttling rate limit"
  type        = number
  default     = 50
}

variable "log_retention_days" {
  description = "Number of days to retain CloudWatch logs"
  type        = number
  default     = 14
}

variable "ecr_repository_url" {
  description = "URL of the ECR repository for the Lambda Docker image"
  type        = string
  default     = "030764292549.dkr.ecr.us-east-1.amazonaws.com/fastapi-lambda"
}
