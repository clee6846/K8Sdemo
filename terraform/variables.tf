variable "peer_owner_id" {
  describe = "AWS account id"
  default = "742886329884"
}

# parms file for aws ec2 cloud
variable "aws_region" {
  description = "AWS region to launch servers."
  default     = "us-west-2"
}


# parms file for aws ec2 cloud


#### VPC Network
variable "vpc_cidr" {
  type    = string
  default = "10.100.0.0/16"
}


#### HTTP PARAMS
variable "network_http1" {
  type = map(string)
  default = {
    subnet_name = "subnet_http1"
    cidr        = "10.100.0.0/20"
  }
}
variable "network_http2" {
  type = map(string)
  default = {
    subnet_name = "subnet_http2"
    cidr        = "10.100.16.0/20"
  }
}
variable "network_http3" {
  type = map(string)
  default = {
    subnet_name = "subnet_http3"
    cidr        = "10.100.32.0/20"
  }
}

# Set number of instance
variable "http1_instance_names" {
  type    = set(string)
  default = ["instance-http1-1"]
}

# Set number of instance
variable "http2_instance_names" {
  type    = set(string)
  default = ["instance-http2-1"]
}

# Set number of instance
variable "http3_instance_names" {
  type    = set(string)
  default = ["instance-http3-1"]
}
