resource "google_project_service" "sqladmin" {
  service = "sqladmin.googleapis.com"

  disable_on_destroy = false
}

resource "google_sql_database_instance" "postgres" {
  name = "message-instance"
  database_version = "POSTGRES_15"
  region = var.region

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = true
    }
    availability_type = "ZONAL"
    backup_configuration {
      enabled = false
    }
  }

  depends_on = [ google_project_service.sqladmin ]
}

resource "google_sql_database" "app_database" {
  name     = var.db_name
  instance = google_sql_database_instance.postgres.name
}

resource "google_sql_user" "app_user" {
  name = var.db_user
  instance = google_sql_database_instance.postgres.name
  password = var.db_password
}

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

resource "google_cloud_run_service" "frontend" {
  name = "frontend-service"
  location = var.region
  project  = var.project

  template {
    metadata {
      annotations = {
        "run.googleapis.com/launch-stage" = "BETA"
        "autoscaling.knative.dev/maxScale" = "1"
        "client.knative.dev/user-image"   = "${var.dockerhub_username}/${var.frontend_image}:${var.image_tag}"
      }
    }
    spec {
      containers {
        image = "${var.dockerhub_username}/${var.frontend_image}:latest"
        ports {
          container_port = 80
        }
        env {
          name  = "BACKEND_URL"
          value = google_cloud_run_service.backend.status[0].url
        }
        env {
          name  = "BACKEND_HOST"
          value = replace(google_cloud_run_service.backend.status[0].url, "https://", "")
        }
      }
    }
  }
  traffic {
    percent = 100
    latest_revision = true
  }

  depends_on = [google_cloud_run_service.backend]
}

resource "google_cloud_run_service_iam_member" "backend_public" {
  service  = google_cloud_run_service.backend.name
  location = var.region
  project  = var.project
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_service_iam_member" "frontend_public" {
  service  = google_cloud_run_service.frontend.name
  location = var.region
  project  = var.project
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_project_iam_member" "cloud_run_sql_client" {
  project = var.project
  role = "roles/cloudsql.client"
  member = "serviceAccount:${data.google_project.current.number}-compute@developer.gserviceaccount.com"
}

data "google_project" "current" {}