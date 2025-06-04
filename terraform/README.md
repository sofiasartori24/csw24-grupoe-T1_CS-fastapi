# AWS Infrastructure for FastAPI Application

This directory contains Terraform configuration for deploying the FastAPI application to AWS. The infrastructure includes:

- VPC with private subnets
- RDS MySQL database
- Lambda function with VPC access
- API Gateway
- IAM roles and security groups
- CloudWatch logs

## Architecture

The architecture follows AWS best practices:

1. **VPC and Networking**:
   - The application runs in a VPC with private subnets
   - Security groups control access between components

2. **Database**:
   - RDS MySQL instance in private subnets
   - Security group allows access only from Lambda

3. **Application**:
   - Lambda function with VPC access to the database
   - API Gateway provides HTTP endpoints
   - CloudWatch logs for monitoring

4. **Security**:
   - IAM roles with least privilege
   - Security groups with restricted access
   - Environment variables for configuration

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform v1.0 or later
- Existing VPC with private subnets

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

- The RDS instance is configured with deletion protection by default. Set `db_deletion_protection = false` in `terraform.tfvars` to allow deletion.
- The Lambda function is configured with VPC access to connect to the RDS instance. This requires the Lambda function to have the appropriate IAM permissions.
- The API Gateway is configured with CORS to allow cross-origin requests.
- CloudWatch logs are configured to retain logs for 14 days by default.

## Improvements

The following improvements have been made to the previous configuration:

1. **VPC Configuration**:
   - Properly configured VPC access for Lambda
   - Used variables for VPC and subnet IDs

2. **RDS Configuration**:
   - Created a new RDS instance with proper configuration
   - Added security group for RDS with restricted access

3. **Lambda Configuration**:
   - Created IAM role with appropriate permissions
   - Added VPC configuration for Lambda
   - Added environment variables for configuration

4. **Security**:
   - Added proper IAM roles and policies
   - Restricted security group access
   - Added tags to all resources

5. **Monitoring**:
   - Added CloudWatch logs for Lambda
   - Configured API Gateway with detailed metrics