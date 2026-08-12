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