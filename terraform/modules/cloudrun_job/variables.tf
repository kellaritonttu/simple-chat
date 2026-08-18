variable "name"   { type = string }

variable "region" { type = string }

variable "image"  { type = string }

variable "service_account_name" { type = string }

variable "sql_connection_name"  { type = string }

variable "env_vars" { 
  type = map(string)
  default = {} 
}
