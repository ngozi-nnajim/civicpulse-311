resource "azurerm_resource_group" "main" {
  name     = "civicpulse-311-rg"
  location = "uksouth"
}

resource "azurerm_storage_account" "main" {
  name                     = "civicpulse311storage"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "raw" {
  name                  = "raw"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "civicpulse-311-postgres"
  resource_group_name    = azurerm_resource_group.main.name
  location                = azurerm_resource_group.main.location
  version                 = "16"
  administrator_login     = "civicpulse_admin"
  administrator_password  = var.postgres_admin_password
  sku_name                = "B_Standard_B1ms"
  storage_mb              = 32768
  zone                    = "1"
}

resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = "civicpulse"
  server_id = azurerm_postgresql_flexible_server.main.id
  collation = "en_US.utf8"
  charset   = "UTF8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_my_ip" {
  name             = "allow-my-ip"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = "86.22.115.96"
  end_ip_address   = "86.22.115.96"
}
