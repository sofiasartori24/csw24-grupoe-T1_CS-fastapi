variable "ami_id" {
  description = "ID da imagem AMI"
  default     = "ami-0c55b159cbfafe1f0"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_name" {
  description = "Nome da chave SSH"
  default     = "construcao"
}

# variables.tf

variable "vpc_id" {
  description = "ID da VPC onde RDS e Lambda rodarão"
  type        = string
}

variable "private_subnet_ids" {
  description = "Lista de IDs das subnets privadas onde RDS e Lambda ficarão"
  type        = list(string)
}

variable "db_name" {
  description = "Nome do banco de dados MySQL"
  type        = string
  default     = "resources_management"
}

variable "db_username" {
  description = "Usuário MySQL"
  type        = string
  default     = "user"
}

variable "db_password" {
  description = "Senha do usuário MySQL"
  type        = string
  default     = "password"
}
