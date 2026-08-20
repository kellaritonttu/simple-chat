module "iam" {
  source = "./modules/iam"

  project = var.project
  service_account_id = var.service_account_id
}

module "cloudsql" {
  source = "./modules/cloud_sql"
  
  instance_name = "message-instance"
  db_user       = var.db_user
  db_password   = var.db_password
  db_name       = var.db_name
  region        = var.region
}

module "firebase" {
  source = "./modules/firebase"

  app_display_name       = var.app_display_name
  authorized_domains     = var.authorized_domains
  google_oauth_client_id = var.google_oauth_client_id
  google_oauth_client_secret = var.google_oauth_client_secret
}

module "migrate" {
  source = "./modules/cloudrun_job"
  
  name   = "db-migrate"
  region = var.region
  image  = local.migrate_image
  
  service_account_name = module.iam.service_account_email
  sql_connection_name  = module.cloudsql.connection_name
  
  env_vars = {
    DATABASE_URL = local.database_url
  }
}

module "backend" {
  source = "./modules/cloudrun_service"

  name      = "backend-service"
  region    = var.region
  image     = local.backend_image
  port      = var.backend_port
  max_scale = 1
  
  sql_connection_name  = module.cloudsql.connection_name
  service_account_name = module.iam.service_account_email

  env_vars = {
    DATABASE_URL        = local.database_url
    FRONTEND_URL        = var.frontend_url
    FIREBASE_PROJECT_ID = var.project
  }

  depends_on = [module.migrate]
}

module "frontend" {
  source = "./modules/cloudrun_service"

  name      = "frontend-service"
  region    = var.region
  image     = local.frontend_image
  port      = var.frontend_port
  max_scale = 1

  service_account_name = module.iam.service_account_email

  env_vars = {
    BACKEND_URL            = module.backend.url
    PUBLIC_FIREBASE_CONFIG = jsonencode({
      apiKey            = module.firebase.api_key
      authDomain        = module.firebase.auth_domain
      projectId         = var.project
      storageBucket     = module.firebase.storage_bucket
      messagingSenderId = module.firebase.messaging_sender_id
      appId             = module.firebase.app_id
    })
  }

  depends_on = [module.backend]
}