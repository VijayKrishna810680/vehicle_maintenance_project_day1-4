variable "project" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "enable_apis" {
  type = list(string)
  default = [
    "sqladmin.googleapis.com",
    "run.googleapis.com",
    "containerregistry.googleapis.com",
    "cloudbuild.googleapis.com"
  ]
}

variable "instance_name" {
  type    = string
  default = "vehicle-psql-instance"
}

variable "db_name" {
  type    = string
  default = "vehicle_maintenance"
}

variable "db_tier" {
  type    = string
  default = "db-f1-micro"
}
