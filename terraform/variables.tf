# __ GCP _______________________________________________________________________

variable "project" {
  type        = string
  description = "GCP Project ID"
  sensitive   = true
}

variable "region" {
  type        = string
  description = "GCP Region"
  default     = "us-west1"
}

variable "service_account_id" {
  type        = string
  description = "Service account ID for Cloud Run"
  default     = "cloud-run-sa"
}

# __ Cloud SQL _________________________________________________________________

variable "db_name" {
  type        = string
  description = "Cloud SQL database name"
  default     = "chat_db"
}

variable "db_user" {
  type        = string
  description = "Cloud SQL user"
  default     = "admin"
}

variable "db_password" {
  type        = string
  description = "Cloud SQL password"
  sensitive   = true
}


# __ Docker Hub ________________________________________________________________

variable "dockerhub_username" {
  type        = string
  description = "Docker Hub username"
}

variable "backend_image" {
  type        = string
  description = "Backend image name on Docker Hub"
}

variable "frontend_image" {
  type        = string
  description = "Frontend image name on Docker Hub"
}

variable "migrate_image" {
  type        = string
  description = "Migration image name on Docker Hub"
}

variable "image_tag" {
  type        = string
  description = "Docker image tag to deploy"
  default     = "latest"
}


# __ Cloud Run _________________________________________________________________

variable "frontend_port" {
  type        = number
  description = "Frontend Cloud Run port"
  default     = 3000
}

variable "backend_port" {
  type        = number
  description = "Backend Cloud Run port"
  default     = 8000
}

variable "frontend_url" {
  type        = string
  description = "Allowed frontend origin for CORS"
  default     = "*"
}


# __ Firebase __________________________________________________________________

variable "app_display_name" {
  type        = string
  description = "Firebase Web App for a Simple-App Auth"
  default = "Simple-App Auth"
}

variable "google_oauth_client_id" {
  type        = string
  description = "Google OAuth 2.0 client ID for Firebase sign-in"
  sensitive   = true
}

variable "google_oauth_client_secret" {
  type        = string
  description = "Google OAuth 2.0 client secret for Firebase sign-in"
  sensitive   = true
}

variable "authorized_domains" {
  type        = list(string)
  description = "Domains authorized for Firebase Auth OAuth redirects"
  default     = ["localhost"]
}