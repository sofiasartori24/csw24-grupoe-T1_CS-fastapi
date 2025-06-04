# Terraform Infrastructure as Code (IaC)

This directory contains Terraform configuration files to provision the entire infrastructure for the FastAPI application on AWS, including:

- RDS MySQL database
- Lambda function
- API Gateway
- IAM roles and policies
- Security groups

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) installed (version >= 1.0)
- AWS credentials configured
- Basic knowledge of Terraform and AWS
- S3 bucket for Terraform state (for production deployments)

## Configuration

1. Update the `terraform.tfvars` file with your specific values:
   - `vpc_id`: Your VPC ID
   - `private_subnet_ids`: List of your private subnet IDs
   - `db_name`, `db_username`, `db_password`: Database credentials
   - Other variables as needed

## Usage

### Local Development

1. Initialize Terraform:
   ```bash
   terraform init
   ```

2. Plan the deployment:
   ```bash
   terraform plan
   ```

3. Apply the changes:
   ```bash
   terraform apply
   ```

4. To destroy the infrastructure:
   ```bash
   terraform destroy
   ```

### Production Deployment with S3 Backend

1. Create an S3 bucket for Terraform state:
   ```bash
   aws s3 mb s3://your-terraform-state-bucket
   ```

2. Initialize Terraform with the S3 backend:
   ```bash
   terraform init \
     -backend-config="bucket=your-terraform-state-bucket" \
     -backend-config="key=resources-management/terraform.tfstate" \
     -backend-config="region=us-east-1"
   ```

3. Plan and apply as usual:
   ```bash
   terraform plan
   terraform apply
   ```

## CI/CD Integration

This Terraform configuration is designed to work with the GitHub Actions CI/CD pipeline. The pipeline:

1. Sets up AWS credentials
2. Creates a `terraform.auto.tfvars` file with values from GitHub Secrets
3. Initializes Terraform with the S3 backend
4. Validates, plans, and applies the Terraform configuration
5. Tests the deployed API

Required GitHub Secrets for CI/CD:
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`
- `VPC_ID`, `SUBNET_ID_1`, `SUBNET_ID_2`
- `DB_USERNAME`, `DB_PASSWORD`
- `TF_STATE_BUCKET`

## Outputs

After successful deployment, Terraform will output:
- `rds_endpoint`: The endpoint of the RDS MySQL instance
- `api_gateway_url`: The URL of the API Gateway endpoint
- `lambda_function_name`: The name of the Lambda function
- `lambda_function_arn`: The ARN of the Lambda function

## Resources Created

- **Database**:
  - RDS MySQL instance
  - DB subnet group
  - Security group for RDS

- **Lambda**:
  - Lambda function with the FastAPI application
  - IAM role and policies
  - Security group for Lambda

- **API Gateway**:
  - HTTP API Gateway
  - Routes for the API
  - Integration with Lambda
  - Deployment stage

## Notes

- The Lambda function is configured to use the RDS MySQL instance
- The API Gateway is configured to route all requests to the Lambda function
- The Lambda function has the necessary permissions to access the RDS instance