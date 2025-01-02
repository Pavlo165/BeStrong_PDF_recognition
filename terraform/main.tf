# 📦 Creating a Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.resource_group_name}-${terraform.workspace}"   # 🏷️ Name of the Resource Group
  location = var.location              # 🌍 Azure region where resources will be created
}

# 📦 Storage Account
resource "azurerm_storage_account" "storage_account" {
  name                     = "${var.storage-name}env${terraform.workspace}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
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
  storage_account_id = azurerm_storage_account.storage_account.id
  quota                = 50
}

# 📦 App Service Plan
resource "azurerm_app_service_plan" "app_service_plan" {
  name                = "infra-service-plan-${terraform.workspace}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "FunctionApp"
  reserved            = true
  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

# 📦 Linux Function App for Python
resource "azurerm_linux_function_app" "function_app" {
  name                       = "infra-function-app-${terraform.workspace}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  service_plan_id            = azurerm_app_service_plan.app_service_plan.id
  storage_account_name       = azurerm_storage_account.storage_account.name
  storage_account_access_key = azurerm_storage_account.storage_account.primary_access_key

  site_config {
    application_stack {
      python_version = "3.9" # Вказуємо версію 3.9 Python
    }
  }

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME"          = "python" # runtime
    "WEBSITE_RUN_FROM_PACKAGE"          = "1"     # Налаштування для запуску із пакету 
    "AZURE_STORAGE_CONNECTION_STRING"   = azurerm_storage_account.storage_account.primary_connection_string
    "AZURE_FILE_SHARE_NAME"             = azurerm_storage_share.file_share.name
    "AZURE_FILE_PATH"                   = "/path/to/your/file" # Replace with actual file path?
    "AZURE_BLOB_CONTAINER_NAME"         = azurerm_storage_container.blob_container.name
    "AZURE_FORM_RECOGNIZER_ENDPOINT"    = azurerm_cognitive_account.document_intelligence.endpoint
    "AZURE_FORM_RECOGNIZER_KEY"         = azurerm_cognitive_account.document_intelligence.primary_access_key
  }

  identity {
    type = "SystemAssigned"
  }
}

# 📦 Cognitive Services Account
resource "azurerm_cognitive_account" "document_intelligence" {
  name                = "infra-ai-doc-intelligence-${terraform.workspace}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "FormRecognizer"
  sku_name            = "S0"
}