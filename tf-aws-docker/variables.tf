variable "access_key" {
	default = "AKIAJOICH7L4GJP3CBNQ"
}
variable "secret_key" {
	default = "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"
}
variable "region" {
    default = "us-west-2"
}
variable "key_path" {
  description = "SSH Public Key path"
  default     = "/Users/svaliveru/.ssh/sigmaex2KeyPair.pub"
}
variable "private_key_path" {
  description = "SSH Private Key path"
  default     = "/Users/svaliveru/.ssh/sigmaex2KeyPair.pem"
}

variable "ami" {
  description = "Ubuntu"
  default     = "ami-1ee65166"
}

variable "SWARM_NAME" {
  default = "aws-docker"
}

variable "KEYNAME" {
  default = "SwarmKeyPair"
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
  default = 2
}

variable "WORKERDISKTYPE" {
  default = "standard"
}

variable "WORKERDISKSIZE" {
  default = 20
}
