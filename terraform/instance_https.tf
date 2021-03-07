#### INSTANCE Admin ####
  
# Create instance
resource "aws_instance" "http1" {
  for_each      = var.http1_instance_names
  ami           = var.aws_amis[var.aws_region]
  instance_type = "t3.medium"
  key_name      = "tester2"
  vpc_security_group_ids = [
    aws_security_group.administration.id,
    aws_security_group.web.id,
  ]
  subnet_id = aws_subnet.http1.id
  tags = {
    Name = each.key
  }
}


# Attach floating ip on instance http
resource "aws_eip" "public_http1" {
  for_each   = var.http1_instance_names
  vpc        = true
  instance   = aws_instance.http1[each.key].id
  depends_on = [aws_internet_gateway.gw]
  tags = {
    Name = "public-http1-${each.key}"
  }
}
# Create instance
resource "aws_instance" "http2" {
  for_each      = var.http2_instance_names
  ami           = var.aws_amis[var.aws_region]
  instance_type = "t3.medium"
  key_name      = "tester2"
  vpc_security_group_ids = [
    aws_security_group.administration.id,
    aws_security_group.web.id,
  ]
  subnet_id = aws_subnet.http2.id
  tags = {
    Name = each.key
  }
}


# Attach floating ip on instance http
resource "aws_eip" "public_http2" {
  for_each   = var.http2_instance_names
  vpc        = true
  instance   = aws_instance.http2[each.key].id
  depends_on = [aws_internet_gateway.gw]
  tags = {
    Name = "public-http2-${each.key}"
  }
}

# Create instance
resource "aws_instance" "http3" {
  for_each      = var.http3_instance_names
  ami           = var.aws_amis[var.aws_region]
  instance_type = "t3.medium"
  key_name      = "tester2"
  vpc_security_group_ids = [
    aws_security_group.administration.id,
    aws_security_group.web.id,
  ]
  subnet_id = aws_subnet.http3.id
  tags = {
    Name = each.key
  }
}

# Attach floating ip on instance http
resource "aws_eip" "public_http3" {
  for_each   = var.http3_instance_names
  vpc        = true
  instance   = aws_instance.http3[each.key].id
  depends_on = [aws_internet_gateway.gw]
  tags = {
    Name = "public-http3-${each.key}"
  }
}

