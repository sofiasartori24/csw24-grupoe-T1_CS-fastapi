# VPC and Subnet Configuration
vpc_id = "vpc-0f53830436b086840"  # Use the actual VPC ID from the previous configuration
private_subnet_ids = [
  "subnet-094b48a14e397a2e8",
  "subnet-0722195fdb9cc24a9",
  "subnet-0c5f6ffdd0abc5587"
]  # Use the actual subnet IDs from the previous configuration

# Database Configuration
db_name     = "resources_management"
db_username = "user"
db_password = "password"  # Use a secure password in production
db_pool_size = "5"
db_max_overflow = "10"
db_pool_recycle = "300"

# Security Group and IAM Configuration
rds_security_group_id = "sg-087e6b149c05647f2"  # RDS security group ID from previous configuration
lambda_role_arn = "arn:aws:iam::030764292549:role/LabRole"  # Lambda role ARN from previous configuration

# Lambda Configuration
lambda_memory_size = 512
lambda_timeout     = 60
lambda_runtime     = "python3.9"

# API Gateway Configuration
api_stage_name = "Prod"
api_throttling_burst_limit = 100
api_throttling_rate_limit = 50

# General Configuration
region = "us-east-1"
environment = "dev"
project_name = "resources-management"
debug_mode = "true"
log_level = "DEBUG"
api_version = "1.0.0"
log_retention_days = 14