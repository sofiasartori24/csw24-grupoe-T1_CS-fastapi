output "vpc_id" {
  description = "ID of the VPC"
  value       = var.vpc_id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = var.private_subnet_ids
}

output "rds_endpoint" {
  description = "Endpoint of the RDS MySQL instance"
  value       = aws_db_instance.rds.address
}

output "rds_port" {
  description = "Port of the RDS MySQL instance"
  value       = aws_db_instance.rds.port
}

output "rds_name" {
  description = "Name of the RDS MySQL instance"
  value       = aws_db_instance.rds.db_name
}

output "rds_username" {
  description = "Username for the RDS MySQL instance"
  value       = aws_db_instance.rds.username
  sensitive   = true
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.fastapi_lambda.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.fastapi_lambda.arn
}

output "lambda_invoke_arn" {
  description = "Invoke ARN of the Lambda function"
  value       = aws_lambda_function.fastapi_lambda.invoke_arn
}

output "lambda_environment_variables" {
  description = "Environment variables set in the Lambda function"
  value       = aws_lambda_function.fastapi_lambda.environment[0].variables
  sensitive   = true
}

output "lambda_security_group_id" {
  description = "ID of the Lambda security group"
  value       = aws_security_group.lambda_sg.id
}

output "rds_security_group_id" {
  description = "ID of the RDS security group"
  value       = aws_security_group.rds_sg.id
}

output "api_gateway_id" {
  description = "ID of the API Gateway"
  value       = aws_apigatewayv2_api.api_gateway.id
}

output "api_gateway_stage_name" {
  description = "Name of the API Gateway stage"
  value       = aws_apigatewayv2_stage.api_stage.name
}

output "api_gateway_url" {
  description = "URL of the API Gateway endpoint"
  value       = aws_apigatewayv2_stage.api_stage.invoke_url
}

output "api_gateway_endpoint" {
  description = "Full endpoint URL for the API"
  value       = "${aws_apigatewayv2_stage.api_stage.invoke_url}/"
}

output "cloudwatch_log_group" {
  description = "Name of the CloudWatch log group for Lambda"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}

output "lambda_role_arn" {
  description = "ARN of the Lambda execution role"
  value       = aws_iam_role.lambda_role.arn
}

output "lambda_role_name" {
  description = "Name of the Lambda execution role"
  value       = aws_iam_role.lambda_role.name
}
