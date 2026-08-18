terraform {
    required_version = ">= 1.0.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 6.0"
    }
  }

  cloud {
    organization = "kellaritonttu"

    workspaces {
      name = "simple-chat"
    }
  }
}