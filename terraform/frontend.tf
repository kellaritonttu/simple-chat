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
      service_account_name = google_service_account.cloud_run.email
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
        env {
          name  = "PUBLIC_FIREBASE_API_KEY"
          value = var.apiKey
        }
        env {
          name  = "PUBLIC_FIREBASE_AUTH_DOMAIN"
          value = var.authDomain
        }
        env {
          name  = "PUBLIC_FIREBASE_PROJECT_ID"
          value = var.projectId
        }
        env {
          name  = "PUBLIC_FIREBASE_MESSAGING_SENDER"
          value = var.messagingSenderId
        }
        env {
          name  = "PUBLIC_FIREBASE_APP_ID"
          value = var.appId
        }
        env {
          name  = "PUBLIC_FIREBASE_STORAGE_BUCKET"
          value = var.storageBucket
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


resource "google_cloud_run_service_iam_member" "frontend_public" {
  service  = google_cloud_run_service.frontend.name
  location = var.region
  project  = var.project
  role     = "roles/run.invoker"
  member   = "allUsers"
}