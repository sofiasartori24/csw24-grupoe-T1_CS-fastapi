output "rds_endpoint" {
  description = "Endpoint da instância RDS MySQL"
  value       = aws_db_instance.mydb.address
}
