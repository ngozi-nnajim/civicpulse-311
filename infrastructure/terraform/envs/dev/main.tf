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
