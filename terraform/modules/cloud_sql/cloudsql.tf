resource "google_project_service" "sqladmin" {
  service = "sqladmin.googleapis.com"

  disable_on_destroy = false
}

resource "google_sql_database_instance" "this" {
  name   = var.instance_name
  region = var.region
  
  database_version = "POSTGRES_15"
  
  settings {
    tier = var.tier
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

resource "google_sql_database" "this" {
  name     = var.db_name
  instance = google_sql_database_instance.this.name
}

resource "google_sql_user" "this" {
  name = var.db_user
  instance = google_sql_database_instance.this.name
  password = var.db_password
}