terraform {
  backend "s3" {
    bucket = "gabriel-terraform-state-2026"
    key    = "infra/terraform.tfstate"
    region = "us-east-1"
  }
}
