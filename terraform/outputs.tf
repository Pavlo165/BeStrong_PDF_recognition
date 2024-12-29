# Output для Storage Account
output "storage_account_name" {
  description = "The name of the created Storage Account"
  value       = azurerm_storage_account.storage_account.name
}

output "storage_account_primary_key" {
  description = "The primary access key of the Storage Account"
  value       = azurerm_storage_account.storage_account.primary_access_key
  sensitive   = true
}

# Output для Storage Container
output "blob_container_name" {
  description = "The name of the created Blob Container"
  value       = azurerm_storage_container.blob_container.name
}

# Output для App Service Plan
output "app_service_plan_name" {
  description = "The name of the created App Service Plan"
  value       = azurerm_app_service_plan.app_service_plan.name
}

# Output для Linux Function App
output "function_app_name" {
  description = "The name of the created Linux Function App"
  value       = azurerm_linux_function_app.function_app.name
}

output "function_app_default_hostname" {
  description = "The default hostname of the Function App"
  value       = azurerm_linux_function_app.function_app.default_hostname
}

# Output для Cognitive Services Account
output "cognitive_account_name" {
  description = "The name of the created Cognitive Services Account"
  value       = azurerm_cognitive_account.document_intelligence.name
}

output "cognitive_account_endpoint" {
  description = "The endpoint of the Cognitive Services Account"
  value       = azurerm_cognitive_account.document_intelligence.endpoint
}

output "cognitive_account_api_keys" {
  description = "The API keys of the Cognitive Services Account"
  value       = azurerm_cognitive_account.document_intelligence.primary_access_key
  sensitive   = true
}
