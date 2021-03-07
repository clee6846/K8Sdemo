  
# VPC creation
resource "aws_vpc" "terraform" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  tags = {
    Name = "vpc-terraform"
  }
}

# http subnet configuration
resource "aws_subnet" "http1" {
  vpc_id     = aws_vpc.terraform.id
  cidr_block = var.network_http1["cidr"]
  tags = {
    Name = "subnet-http1"
  }
  depends_on = [aws_internet_gateway.gw]
}
# http subnet configuration
resource "aws_subnet" "http2" {
  vpc_id     = aws_vpc.terraform.id
  cidr_block = var.network_http2["cidr"]
  tags = {
    Name = "subnet-http2"
  }
  depends_on = [aws_internet_gateway.gw]
}
# http subnet configuration
resource "aws_subnet" "http3" {
  vpc_id     = aws_vpc.terraform.id
  cidr_block = var.network_http3["cidr"]
  tags = {
    Name = "subnet-http3"
  }
  depends_on = [aws_internet_gateway.gw]
}
# External gateway configuration
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.terraform.id
  tags = {
    Name = "internet-gateway"
  }
}

