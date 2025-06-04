# AWS Infrastructure for FastAPI Application

This directory contains Terraform configuration for deploying the FastAPI application to AWS. The infrastructure includes:

- Lambda function with VPC access to an existing RDS database
- API Gateway for HTTP endpoints
- Security groups for proper network access
- CloudWatch logs for monitoring

## Architecture

The architecture follows AWS best practices:

1. **VPC and Networking**:
   - The application runs in an existing VPC with private subnets
   - Security groups control access between components

2. **Database**:
   - Uses an existing RDS MySQL instance
   - Security group rules allow access only from Lambda

3. **Application**:
   - Lambda function with VPC access to the database
   - API Gateway provides HTTP endpoints
   - CloudWatch logs for monitoring

4. **Security**:
   - Uses existing IAM roles with appropriate permissions
   - Security groups with restricted access
   - Environment variables for configuration

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform v1.0 or later
- Existing VPC with private subnets
- Existing RDS MySQL instance

## Configuration

The infrastructure is configured using the following files:

- `main.tf`: Main infrastructure configuration
- `variables.tf`: Variable definitions
- `terraform.tfvars`: Variable values
- `outputs.tf`: Output values
- `provider.tf`: Provider configuration

## Deployment

To deploy the infrastructure:

1. Update `terraform.tfvars` with your desired configuration
2. Initialize Terraform:
   ```
   terraform init
   ```
3. Plan the deployment:
   ```
   terraform plan
   ```
4. Apply the changes:
   ```
   terraform apply
   ```

## Cleanup

To destroy the infrastructure:

```
terraform destroy
```

## Important Notes

- This configuration uses existing resources (VPC, subnets, RDS, IAM role) rather than creating new ones
- The Lambda function is configured with VPC access to connect to the RDS instance
- The API Gateway is configured with CORS to allow cross-origin requests
- CloudWatch logs are configured to retain logs for 14 days by default

## Improvements Made

The following improvements have been made to the previous configuration:

1. **VPC Configuration**:
   - Properly configured VPC access for Lambda using variables
   - Used subnet IDs from variables for better flexibility

2. **Security Group Configuration**:
   - Created a dedicated security group for Lambda
   - Added a security group rule to allow Lambda to access RDS

3. **Lambda Configuration**:
   - Used environment variables for configuration
   - Added proper VPC configuration for database access
   - Configured CloudWatch logs with retention policy

4. **API Gateway Configuration**:
   - Added CORS support
   - Configured throttling and metrics
   - Added proper routes for the API

5. **Resource Tagging**:
   - Added tags to all resources for better management
   - Included environment and project information