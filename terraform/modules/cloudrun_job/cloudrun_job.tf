resource "google_cloud_run_v2_job" "this" {
  name     = var.name
  location = var.region

  template {
    template {
      service_account = var.service_account_name

      containers {
        image = var.image

        dynamic "env" {
          for_each = var.env_vars
          content {
            name  = env.key
            value = env.value
          }
        }

        volume_mounts {
          name       = "cloudsql"
          mount_path = "/cloudsql"
        }
      }

      volumes {
        name = "cloudsql"
        cloud_sql_instance {
          instances = [var.sql_connection_name]
        }
      }
    }
  }
}