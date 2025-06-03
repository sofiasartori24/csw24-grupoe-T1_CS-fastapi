
resource "aws_db_subnet_group" "default" {
  name       = "rds-subnet-group"
  subnet_ids = var.private_subnet_ids
}

resource "aws_security_group" "rds_sg" {
  name   = "rds_sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    # A SAS da Lambda vai no Security Group a seguir
    security_groups = [aws_security_group.lambda_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "lambda_sg" {
  name   = "lambda_sg"
  vpc_id = var.vpc_id
}

resource "aws_db_instance" "mydb" {
  identifier             = "meu-db-instance"
  allocated_storage      = 20
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"

  db_name                = var.db_name       # ← use db_name, não name
  username               = var.db_username
  password               = var.db_password

  parameter_group_name   = "default.mysql8.0"
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot    = true
  publicly_accessible    = false
  deletion_protection    = false
  backup_retention_period = 7
}


//instancia rds de mysql
//gerar um template do cloudFormation para api labda
//comando aws sam
// queremos Usar Terraform só para RDS e SAM/CloudFormation para Lambda + API