terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.76.0"
    }
  }
}


provider "aws" {
  region = var.AWS_REGION_NAME
}
