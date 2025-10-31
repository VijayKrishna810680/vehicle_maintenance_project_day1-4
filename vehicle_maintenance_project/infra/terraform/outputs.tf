output "instance_connection_name" {
  description = "Cloud SQL instance connection name"
  value       = google_sql_database_instance.postgres.connection_name
}

output "instance_public_ip" {
  description = "Cloud SQL public IP address"
  value       = google_sql_database_instance.postgres.ip_address[0].ip_address
}

output "db_root_password" {
  description = "Generated DB root password (store this securely)"
  value       = random_password.db_password.result
  sensitive   = true
}
