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
        image = "${var.dockerhub_username}/${var.frontend_image}:${var.image_tag}"
        ports {
          container_port = 3000
        }
        env {
          name  = "BACKEND_URL"
          value = google_cloud_run_service.backend.status[0].url
        }
        env {
          name  = "PUBLIC_FIREBASE_CONFIG"
          value = jsonencode({
            apiKey            = var.apiKey
            authDomain        = var.authDomain
            projectId         = var.projectId
            storageBucket     = var.storageBucket
            messagingSenderId = var.messagingSenderId
            appId             = var.appId
          })
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