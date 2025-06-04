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
  backend "s3" {
    # These values will be filled in by the CI/CD pipeline
    # using -backend-config parameters
  }
}
