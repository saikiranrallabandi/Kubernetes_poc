/* Setup our aws provider */
provider "aws" {
  access_key  = "${var.access_key}"
  secret_key  = "${var.secret_key}"
  region      = "${var.region}"
}
resource "aws_instance" "master" {
  ami           = "${var.ami}"
  instance_type          = "${var.MANAGERINSTANCETYPE}"
  security_groups = ["${aws_security_group.swarm.name}"]
  key_name = "${aws_key_pair.deployer.key_name}"
//  ebs_block_device {
 //   device_name = "/dev/xvdb"
  //  volume_size = "${var.MANAGERDISKSIZE}"
   // volume_type = "${var.MANAGERDISKTYPE}"
  //}
  connection {
    user = "ubuntu"
    private_key = "${file(var.private_key_path)}"
  }
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
      "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"",
      "sudo apt-get update",
      "sudo apt-cache policy docker-ce",
      "sudo apt-get update",
      "sudo apt-get install -y docker-ce",
      "sudo docker swarm init",
      "sudo docker swarm join-token --quiet worker > /home/ubuntu/token",
      "sudo docker run -p 2375:2375 -d -v /var/run/docker.sock:/var/run/docker.sock jarkt/docker-remote-api",
      "sudo docker service create --name=viz  --publish=8080:8080/tcp  --constraint=node.role==manager  --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock dockersamples/visualizer"
    ]
  }
  tags = { 
    Name = "${var.SWARM_NAME}-master"
  }
}

resource "aws_instance" "slave" {
  count         = "${var.CLUSTERSIZE}"
  ami           = "${var.ami}"
  instance_type = "${var.INSTANCETYPE}"
  security_groups = ["${aws_security_group.swarm.name}"]
  key_name = "${aws_key_pair.deployer.key_name}"
  //ebs_block_device {
   // device_name = "/dev/xvdb"
    //volume_size = "${var.WORKERDISKSIZE}"
    //volume_type = "${var.WORKERDISKTYPE}"
 // }
  connection {
    user = "ubuntu"
    private_key = "${file(var.private_key_path)}"
  }
 provisioner "file" {
    source = "${var.private_key_path}"
    destination = "/home/ubuntu/.ssh/key.pem"
  }
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
      "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"",
      "sudo apt-get update",
      "sudo apt-cache policy docker-ce",
      "sudo apt-get update",
      "sudo apt-get install -y docker-ce",
      "sudo chmod 400 /home/ubuntu/.ssh/key.pem",
      "sudo scp -o StrictHostKeyChecking=no -o NoHostAuthenticationForLocalhost=yes -o UserKnownHostsFile=/dev/null -i /home/ubuntu/.ssh/key.pem ubuntu@${aws_instance.master.private_ip}:/home/ubuntu/token .",
      "sudo docker swarm join --token $(cat /home/ubuntu/token) ${aws_instance.master.private_ip}:2377"
    ]
  }
  tags = { 
    Name = "${var.SWARM_NAME}-worker-${count.index}"
  }
}
