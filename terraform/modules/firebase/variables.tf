variable "app_display_name" {
  type    = string
}

variable "google_oauth_client_id" {
  type      = string
  sensitive = true
}

variable "google_oauth_client_secret" {
  type      = string
  sensitive = true
}

variable "authorized_domains" {
  type    = list(string)
}