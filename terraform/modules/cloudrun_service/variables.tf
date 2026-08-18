# __ CloudRun __________________________________________________________________

variable "name"      { type = string }

variable "region"    { type = string }

variable "image"     { type = string }

variable "max_scale" { type = number }

variable "port"      { type = number }

variable "service_account_name" { type = string }

variable "sql_connection_name" {
  type    = string
  default = ""
}

# __ Environment values ________________________________________________________

variable "env_vars" { 
  type    = map(string)
  default = {} 
}