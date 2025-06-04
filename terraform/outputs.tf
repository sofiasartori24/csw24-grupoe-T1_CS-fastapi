output "rds_endpoint" {
  description = "Endpoint of the RDS MySQL instance"
  value       = data.aws_db_instance.existing.address
}

output "api_gateway_url" {
  description = "URL of the API Gateway endpoint"
  value       = "${aws_apigatewayv2_stage.api_stage.invoke_url}"
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.fastapi_lambda.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.fastapi_lambda.arn
}
