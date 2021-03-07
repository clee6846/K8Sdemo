variable "aws_amis" {
  type = map
  default = {
    "eu-west-1" = "ami-b1cf19c6"
    "us-east-1" = "ami-de7ab6b6"
    "us-west-1" = "ami-005c06c6de69aee84"
    "us-west-2" = "ami-0e999cbd62129e3b1"
  }
}
