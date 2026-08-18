resource "google_cloud_run_service" "this" {
  name =     var.name
  location = var.region

  template {
    metadata {
      annotations = merge(
        {
          "run.googleapis.com/launch-stage"       = "BETA"
          "autoscaling.knative.dev/maxScale"      = var.max_scale
          "client.knative.dev/user-image"         = var.image
        },
        var.sql_connection_name != "" ? {
          "run.googleapis.com/cloudsql-instances" = var.sql_connection_name
        } : {}
      )
    }
    spec {
      service_account_name = var.service_account_name
      containers {
        image = var.image
        ports {
          container_port = var.port
        }
        dynamic "env" {
          for_each = var.env_vars
          content {
            name  = env.key
            value = env.value
          }
        }
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}


resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_service.this.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}