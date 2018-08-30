//output "master.ip" {
 // value = "${aws_instance.master.public_ip}"
//}

output "master_public_ips" {
  description = "List of public IP addresses assigned to the master instances"
  value       = ["${aws_instance.master.*.public_ip}"]
}

output "master_public_dns" {
  description = "List of public DNS names assigned to the instances"
  value       = ["${aws_instance.master.*.public_dns}"]
}

output "slave_public_ips" {
  description = "List of public IP addresses assigned to the slave instances"
  value       = ["${aws_instance.slave.*.public_ip}"]
}

output "slave_public_dns" {
  description = "List of public DNS names assigned to the instances"
  value       = ["${aws_instance.slave.*.public_dns}"]
}
