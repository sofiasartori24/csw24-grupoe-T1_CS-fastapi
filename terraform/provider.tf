provider "aws" {
  region = var.region
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
  
  required_version = ">= 1.0"
  
  # S3 backend configuration for state storage
  # The actual values will be provided via -backend-config in the CI/CD pipeline
  backend "s3" {
    # bucket = "terraform-state-bucket"
    # key    = "resources-management/terraform.tfstate"
    # region = "us-east-1"
    # encrypt = true
  }
}
