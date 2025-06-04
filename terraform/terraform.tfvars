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
db_instance_class = "db.t3.micro"
db_allocated_storage = 20
db_multi_az = false
db_backup_retention_period = 7
db_deletion_protection = false
db_pool_size = "5"
db_max_overflow = "10"
db_pool_recycle = "300"

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