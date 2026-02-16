terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.92"
    }
  }
}

provider "aws" {
  region     = var.region
  access_key = var.access_key
  secret_key = var.secret_key
}

# --- S3 Bucket ---
resource "aws_s3_bucket" "mlops_bucket" {
  bucket = var.bucket_name
}


# --- Network (default VPC) + Security Group ---
data "aws_vpc" "default" {
  default = true
}

# Subnet pública por defecto (si hay varias, cogemos la primera)
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "mlops_sg" {
  name        = "mlops-sg"
  description = "Security group for MLOps EC2"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "FastAPI"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = var.api_cidr_blocks
  }

  ingress {
    description = "MLFlow"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = var.mlflow_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


# --- EC2 ---
resource "aws_instance" "mlops_ec2" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.mlops_sg.id]
  associate_public_ip_address = true

  iam_instance_profile = var.instance_profile_name

  tags = {
    Name = var.instance_name
  }
}
