# Display dns information
  
output "http_ip1" {
  value = {
    for instance in aws_instance.http1 :
    instance.id => instance.private_ip
  }
}
# Display dns information

output "http_ip2" {
  value = {
    for instance in aws_instance.http2 :
    instance.id => instance.private_ip
  }
}
# Display dns information

output "http_ip3" {
  value = {
    for instance in aws_instance.http3 :
    instance.id => instance.private_ip
  }
}
