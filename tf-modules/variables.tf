##General vars
variable "s3_name" {
  default = ""
}

variable "ssh_user" {
  default = "ec2-user"
}

variable "aws_region" {
  description = "AWS region on which we will setup the swarm cluster"
  default     = "us-east-1"
}

variable "ami" {
  description = "Amazon Linux AMI"
  default     = "ami-4fffc834"
}

variable "SWARM_NAME" {
  default = ""
}

variable "KEYNAME" {
  default = "SigmexmKeyPair"
}


# Manager
variable "MANAGERINSTANCETYPE" {
  description = "Manager Instance type"
  default     = "t2.micro"
}

variable "MANAGERSIZE" {
  default = 1
}

variable "MANAGERDISKTYPE" {
  default = "standard"
}

variable "MANAGERDISKSIZE" {
  default = 20
}

# Worker
variable "INSTANCETYPE" {
  description = "Worker Instance type"
  default     = "t2.micro"
}

variable "CLUSTERSIZE" {
  default = 1
}

variable "WORKERDISKTYPE" {
  default = "standard"
}

variable "WORKERDISKSIZE" {
  default = 20
}

variable "key_path" {
  description = "SSH Public Key path"
  default     = "/Users/svaliveru/.ssh/sigmaex2KeyPair.pub"
}

variable "bootstrap_path" {
  description = "Script to install Docker Engine"
  default     = "/Users/svaliveru/sigmaxm-feature2.0/tf-modules/install-docker.sh"
}
