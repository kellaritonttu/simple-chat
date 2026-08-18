output "api_key" {
  value     = data.google_firebase_web_app_config.default.api_key
  sensitive = true
}

output "auth_domain" {
  value = data.google_firebase_web_app_config.default.auth_domain
}

output "app_id" {
  value = google_firebase_web_app.default.app_id
}

output "messaging_sender_id" {
  value = data.google_firebase_web_app_config.default.messaging_sender_id
}

output "storage_bucket" {
  value = lookup(data.google_firebase_web_app_config.default, "storage_bucket", "")
}