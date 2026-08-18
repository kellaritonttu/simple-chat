locals {
  backend_image  = "${var.dockerhub_username}/${var.backend_image}:${var.image_tag}"
  frontend_image = "${var.dockerhub_username}/${var.frontend_image}:${var.image_tag}"
  migrate_image  = "${var.dockerhub_username}/${var.migrate_image}:${var.image_tag}"

  database_url   = "postgresql+asyncpg://${var.db_user}:${var.db_password}@/${module.cloudsql.database_name}?host=/cloudsql/${var.project}:${var.region}:${module.cloudsql.instance_name}"
}