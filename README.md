# Resource Management API

This project is a resource management API for classrooms, buildings, and educational resources, deployed on AWS using Infrastructure as Code (IaC) and CI/CD practices.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Local Development](#local-development)
- [AWS Deployment](#aws-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Testing](#testing)

## Features

- RESTful API for managing educational resources
- Database persistence with MySQL
- AWS Lambda deployment
- Docker containerization
- CI/CD with GitHub Actions
- Infrastructure as Code with Terraform

## Architecture

The application is built with:

- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Deployment**: AWS Lambda + API Gateway
- **Infrastructure**: Terraform
- **CI/CD**: GitHub Actions
- **Containerization**: Docker

## Local Development

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Git

### Running Locally with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/csw24-grupoe-T1_CS-fastapi.git
   cd csw24-grupoe-T1_CS-fastapi
   ```

2. Start the application with Docker Compose:
   ```bash
   docker-compose up
   ```

3. Access the API at http://localhost:8000

4. Access the API documentation at http://localhost:8000/docs

### Running Tests Locally

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest t1_cs/tests/ --cov=t1_cs/app
```

## AWS Deployment

### Prerequisites

- AWS Account
- AWS CLI configured
- Terraform installed

### Manual Deployment with Terraform

1. Set up AWS credentials:
   ```bash
   # Create aws.env file with your credentials
   echo "export AWS_ACCESS_KEY_ID=your_access_key" > aws.env
   echo "export AWS_SECRET_ACCESS_KEY=your_secret_key" >> aws.env
   echo "export AWS_SESSION_TOKEN=your_session_token" >> aws.env
   source aws.env
   ```

2. Update the Terraform variables:
   ```bash
   # Edit terraform/terraform.tfvars with your VPC and subnet IDs
   cd terraform
   nano terraform.tfvars
   ```

3. Deploy the infrastructure with Terraform:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

4. Test the deployed API:
   ```bash
   # Get the API Gateway URL from Terraform outputs
   API_URL=$(terraform output -raw api_gateway_url)
   curl $API_URL
   ```

## CI/CD Pipeline

The project uses GitHub Actions for CI/CD with a workflow defined in `.github/workflows/ci-cd.yml`:

### Workflow Triggers

- **Push to main branch**: Triggers full CI/CD pipeline (build, test, deploy)
- **Pull Requests**: Triggers build and test jobs only

### Pipeline Stages

1. **Build and Test**:
   - Sets up Python 3.9 environment
   - Installs project dependencies
   - Runs unit tests for models, repositories, and services
   - Runs database tests
   - Generates and uploads test coverage reports
   - Builds and tests Docker image

2. **Deploy to AWS** (only on push to main):
   - Configures AWS credentials
   - Sets up Terraform
   - Validates Terraform configuration
   - Plans Terraform changes
   - Applies Terraform changes to provision/update infrastructure
   - Tests the deployed API endpoints
   - Sends deployment notifications

### Error Handling and Notifications

- Failed tests or deployments trigger notifications
- Test results and logs are available in GitHub Actions
- Deployment status is reported via Slack (if configured)

### Required GitHub Secrets

For the CI/CD pipeline to work, you need to set up the following secrets in your GitHub repository:

| Secret Name | Description |
|-------------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key with permissions to deploy resources |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key |
| `DB_USERNAME` | Database username for RDS |
| `DB_PASSWORD` | Database password for RDS |
| `SLACK_WEBHOOK` | (Optional) Webhook URL for Slack notifications |

## Testing

The project includes tests for:

- API endpoints
- Database connections
- Data models

Run tests with:
```bash
pytest t1_cs/tests/ --cov=t1_cs/app
```

## Authors

* Henrique Juchem
* Isabela Guerra
* Lucas Wolschick
* Maria Eduarda Maia
* Sofia Batista Sartori
