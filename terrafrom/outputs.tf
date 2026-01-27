output "ec2_public_ip" {
  value = aws_instance.k3s.public_ip
}

output "ec2_public_dns" {
  value = aws_instance.k3s.public_dns
}

output "ssh_command" {
  value       = "ssh -i generated-key.pem ubuntu@${aws_instance.k3s.public_ip}"
  description = "Copie e cole este comando para acessar a instancia"
}
