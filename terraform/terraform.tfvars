# Default values for the variables
# Replace these with your actual values

vpc_id = "vpc-0123456789abcdef0"
private_subnet_ids = ["subnet-0123456789abcdef0", "subnet-0123456789abcdef1"]

db_name     = "resources_management"
db_username = "user"
db_password = "password"

lambda_memory_size = 512
lambda_timeout     = 60
lambda_runtime     = "python3.9"

region = "us-east-1"