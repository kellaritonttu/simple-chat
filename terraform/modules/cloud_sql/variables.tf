# __ Cloud SQL _________________________________________________________________

variable "instance_name"  { type = string }
variable "db_name"        { type = string }
variable "db_user"        { type = string }

variable "db_password" {
    type = string
    sensitive = true
}

variable "tier"         {
    type = string
    default = "db-f1-micro" 
}


# __ Network variables _________________________________________________________

variable "region" { type = string }