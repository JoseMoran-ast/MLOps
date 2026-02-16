variable "region" {
  type    = string
  default = "eu-north-1"
}

variable "access_key" {
  type      = string
  sensitive = true
}

variable "secret_key" {
  type      = string
  sensitive = true
}

variable "bucket_name" {
  type        = string
  description = "Nombre único del bucket S3"
}

variable "instance_name" {
  type    = string
  default = "mlops-ec2"
}

variable "ami_id" {
  type        = string
  description = "AMI en eu-north-1 (Ubuntu/Amazon Linux)"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "key_name" {
  type        = string
  description = "Nombre del Key Pair existente en AWS"
}

# Para limitar SSH (recomendado: tu IP)
variable "ssh_cidr_blocks" {
  type        = list(string)
  description = "CIDRs permitidos para SSH"
  default     = ["0.0.0.0/0"]
}

# Para exponer la API (puedes limitarlo también)
variable "api_cidr_blocks" {
  type        = list(string)
  description = "CIDRs permitidos para el puerto 8000"
  default     = ["0.0.0.0/0"]
}

variable "mlflow_cidr_blocks" {
  description = "CIDR blocks allowed to access MLflow (port 5000)"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "instance_profile_name" {
  type        = string
  description = "Nombre del IAM Instance Profile (role) adjunto a la EC2"
  default     = null
}
