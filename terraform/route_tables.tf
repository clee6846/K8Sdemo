# Create ande associate route
  
# Routing table configuration
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.terraform.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}
# Associate http1 route
resource "aws_route_table_association" "http1" {
  subnet_id      = aws_subnet.http1.id
  route_table_id = aws_route_table.public.id
}
# Associate http2 route
resource "aws_route_table_association" "http2" {
  subnet_id      = aws_subnet.http2.id
  route_table_id = aws_route_table.public.id
}

# Associate http3 route
resource "aws_route_table_association" "http3" {
  subnet_id      = aws_subnet.http3.id
  route_table_id = aws_route_table.public.id
}


