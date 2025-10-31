terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

resource "google_project_service" "enable_apis" {
  for_each = toset(var.enable_apis)
  service  = each.value
}

resource "random_password" "db_password" {
  length  = 16
  special = true
}

resource "google_sql_database_instance" "postgres" {
  name             = var.instance_name
  database_version = "POSTGRES_15"

  settings {
    tier = var.db_tier
    disk_size = 10
    ip_configuration {
      ipv4_enabled = true
    }
  }

  root_password = random_password.db_password.result
}

resource "google_sql_database" "default_db" {
  name     = var.db_name
  instance = google_sql_database_instance.postgres.name
}

output "instance_connection_name" {
  value = google_sql_database_instance.postgres.connection_name
}

output "instance_public_ip" {
  value = google_sql_database_instance.postgres.ip_address[0].ip_address
}
