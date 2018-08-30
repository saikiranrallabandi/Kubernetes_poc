resource "aws_key_pair" "deployer" {
  key_name = "${var.KEYNAME}"
  public_key = "${file("${var.key_path}")}"

}
