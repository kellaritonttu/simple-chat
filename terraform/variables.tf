# __ GCP _______________________________________________________________________

variable "project" {
  type        = string
  description = "GCP Project ID"
  sensitive   = true
}


# __ Cloud SQL _________________________________________________________________

variable "db_name" {
  description = "Cloud SQL Database Name"
  type        = string
  default     = "messages_db"
}

variable "db_user" {
  description = "Cloud SQL User"
  type        = string
  default     = "app_user"
}

variable "db_password" {
  description = "Cloud SQL Password"
  type        = string
  sensitive   = true
}


# __ Network variables _________________________________________________________

variable "region" {
  type        = string
  description = "GCP Region where our VPC would be"
  default     = "us-west1"
}


# __ DockerHub _________________________________________________________________

variable "dockerhub_username" {
  description = "Docker Hub Username"
  type        = string
}

variable "backend_image" {
  description = "Backend docker image name on Docker Hub"
  type        = string
}

variable "frontend_image" {
  description = "Frontend docker image name on Docker Hub"
  type        = string
}

variable "frontend_url" {
  type        = string
  description = "Allowed frontend origin for CORS"
  default     = "*"
}

variable "image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}