# __ Enable required APIs ______________________________________________________

resource "google_project_service" "firebase" {
  provider                   = google-beta
  service                    = "firebase.googleapis.com"
  disable_dependent_services = false
}

resource "google_project_service" "identitytoolkit" {
  provider = google-beta
  service  = "identitytoolkit.googleapis.com"
  disable_dependent_services = false
}


# __ Enable firebase on project ________________________________________________

resource "google_firebase_project" "default" {
  provider = google-beta

  depends_on = [google_project_service.firebase]
}


# __ Create web app ____________________________________________________________

resource "google_firebase_web_app" "default" {
  provider        = google-beta
  display_name    = var.app_display_name
  deletion_policy = "DELETE"

  depends_on = [google_firebase_project.default]
}


# __ Read generated config _____________________________________________________

data "google_firebase_web_app_config" "default" {
  provider   = google-beta
  web_app_id = google_firebase_web_app.default.app_id
}

# __ Enable identity platform __________________________________________________
# __ Configure sign-in methods _________________________________________________

resource "google_identity_platform_config" "default" {
  provider = google-beta

  autodelete_anonymous_users = false

  sign_in {
    allow_duplicate_emails = false

    anonymous {
      enabled = false
    }

    email {
      enabled           = false
      password_required = false
    }
  }

  authorized_domains = var.authorized_domains

  depends_on = [
    google_firebase_web_app.default,
    google_project_service.identitytoolkit
  ]
}

# __ Enable google sign-in _____________________________________________________

resource "google_identity_platform_default_supported_idp_config" "google" {
  provider      = google-beta
  idp_id        = "google.com"
  client_id     = var.google_oauth_client_id
  client_secret = var.google_oauth_client_secret
  enabled       = true

  depends_on = [google_identity_platform_config.default]
}