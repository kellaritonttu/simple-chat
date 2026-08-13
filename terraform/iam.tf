resource "google_service_account" "cloud_run" {
  account_id = "cloud-run-sa"
  display_name = "Service Account for Cloud Run"
}

resource "google_project_iam_member" "cloud_run_sql_client" {
  project = var.project
  role = "roles/cloudsql.client"
  member = "serviceAccount:${google_service_account.cloud_run.email}"
}

resource "google_project_iam_member" "backend_firebase" {
  project = var.project
  role    = "roles/firebaseauth.admin"
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

data "google_project" "current" {}