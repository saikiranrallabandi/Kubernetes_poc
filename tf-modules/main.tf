##Amazon Infrastructure
provider "aws" {
  region                  = "${var.aws_region}"
  shared_credentials_file = "/Users/svaliveru/.aws/credentials"
}

terraform {
  backend "s3" {
    region  = "us-west-2"
    bucket  = "sigmaxm-tf-bucket"
  }
}

resource "aws_security_group" "default" {
  name = "sg_swarm_cluster"

  # Allow all inbound
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Enable ICMP
  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_key_pair" "default" {
  key_name   = "${var.KEYNAME}"
  public_key = "${file("${var.key_path}")}"
}

resource "aws_instance" "swarm-master" {
  ami                    = "${var.ami}"
  instance_type          = "${var.MANAGERINSTANCETYPE}"
  key_name               = "${aws_key_pair.default.id}"
  user_data              = "${file("${var.bootstrap_path}")}"
  vpc_security_group_ids = ["${aws_security_group.default.id}"]
  count                  = "${var.MANAGERSIZE}"
  tags {
    Name = "${var.SWARM_NAME}-master-${count.index}"
  }
  ebs_block_device {
    device_name = "/dev/xvdb"
    volume_size = "${var.MANAGERDISKSIZE}"
    volume_type = "${var.MANAGERDISKTYPE}"
  }
}

resource "aws_instance" "aws-swarm-workers" {
  ami                    = "${var.ami}"
  instance_type          = "${var.INSTANCETYPE}"
  key_name               = "${aws_key_pair.default.id}"
  user_data              = "${file("${var.bootstrap_path}")}"
  vpc_security_group_ids = ["${aws_security_group.default.id}"]
  count                  = "${var.CLUSTERSIZE}"
  tags {
    Name = "${var.SWARM_NAME}-workers-${count.index}"
  }
  ebs_block_device {
    device_name = "/dev/xvdb"
    volume_size = "${var.WORKERDISKSIZE}"
    volume_type = "${var.WORKERDISKTYPE}"
  }
}
