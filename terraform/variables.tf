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

variable "db_host" {
  description = "Hostname of the existing RDS instance"
  type        = string
  default     = "resources-management-db.xxxxxxxxxx.us-east-1.rds.amazonaws.com"
}
