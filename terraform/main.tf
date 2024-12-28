#====================================================
# 🌟 Authors: Valeriy Manuilyk, Pavlo Mochurad, Liubomyr Shpyrka 🌟
#====================================================
# 🌟 Terraform Configuration for Azure AKS Setup 🌟
#====================================================
# ⚙️ This script provisions an Azure Resource Group 
# and an Azure Kubernetes Service (AKS) cluster.
# ✅ Ensure variables (e.g., `var.resource_group_name`, `var.location`) 
# are properly set in your `terraform.tfvars` file or directly in variables.
# 📂 GitHub: https://github.com/Pavlo165/BeStrong-Terrafrom
#====================================================

# 📦 Creating a Resource Group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name   # 🏷️ Name of the Resource Group
  location = var.location              # 🌍 Azure region where resources will be created
}


resource "azurerm_storage_account" "storage_account" {
  name                     = "storage4252"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "blob_container" {
  name                  = "documents-container"
  storage_account_id    = azurerm_storage_account.storage_account.id
  container_access_type = "private"
}

resource "azurerm_storage_share" "file_share" {
  name                 = "shared-files"
  storage_account_id    = azurerm_storage_account.storage_account.id
  quota                = 50
}

resource "azurerm_function_app" "function_app" {
  name                       = "infra-function-app"
  location                   = var.resource_group_name
  resource_group_name        = var.location
  app_service_plan_id        = azurerm_app_service_plan.app_service_plan.id
  storage_account_name       = azurerm_storage_account.storage_account.name
  storage_account_access_key = azurerm_storage_account.storage_account.primary_access_key
  version                    = "~4"
  os_type                    = "Linux"
}

resource "azurerm_app_service_plan" "app_service_plan" {
  name                = "infra-service-plan"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

resource "azurerm_cognitive_account" "document_intelligence" {
  name                = "infra-ai-doc-intelligence"
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "FormRecognizer"
  sku_name            = "S0"
}