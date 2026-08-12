resource "google_cloud_run_service" "backend" {
  name = "backend-service"
  location = var.region
  project = var.project

  template {
    metadata {
      annotations = {
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.postgres.connection_name
        "run.googleapis.com/launch-stage"       = "BETA"
        "autoscaling.knative.dev/maxScale"      = "1"
        "client.knative.dev/user-image"         = "${var.dockerhub_username}/${var.backend_image}:${var.image_tag}"
      }
    }
    spec {
      service_account_name = google_service_account.cloud_run.email
      containers {
        image = "${var.dockerhub_username}/${var.backend_image}:latest"
        ports {
          container_port = 8000
        }
        env {
          name = "DATABASE_URL"
          value = "postgresql+asyncpg://${var.db_user}:${var.db_password}@/${var.db_name}?host=/cloudsql/${google_sql_database_instance.postgres.connection_name}"
        }
        env {
          name = "FRONTEND_URL"
          value = var.frontend_url
        }
      }
    }
  }
  traffic {
    percent = 100
    latest_revision = true
  }

  depends_on = [ google_sql_database.app_database ]
}


resource "google_cloud_run_service_iam_member" "backend_public" {
  service  = google_cloud_run_service.backend.name
  location = var.region
  project  = var.project
  role     = "roles/run.invoker"
  member   = "allUsers"
}