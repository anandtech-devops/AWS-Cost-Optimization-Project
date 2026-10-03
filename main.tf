resource "aws_instance" "cost_lab" {
  ami           = "ami-01a00762f46d584a1"
  instance_type = "t3.micro"

  tags = {
    name = "cost-optimization-lab"
  }
}