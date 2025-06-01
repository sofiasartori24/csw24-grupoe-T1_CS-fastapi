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
