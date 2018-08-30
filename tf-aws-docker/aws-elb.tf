resource "aws_elb" "service" {
  name                      = "service-${var.name}"
  subnets                   = ["${var.subnet_ids}"]
  cross_zone_load_balancing = true
  internal                  = true

  # Pass it in as a list.
  listener = ["${var.service_ports}"]

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    interval            = 30
    timeout             = 5
    target              = "${var.service_check_target}"
  }

  tags {
    Name        = "service-${var.name}"
    Environment = "${var.environment}"
    Service     = "${var.name}"
  }
}
