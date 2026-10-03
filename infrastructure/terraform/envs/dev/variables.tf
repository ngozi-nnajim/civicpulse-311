variable "postgres_admin_password" {
  description = "Admin password for the PostgreSQL server"
  type        = string
  sensitive   = true
}
