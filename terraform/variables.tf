#====================================================
# 🌟 Authors: Valeriy Manuilyk, Pavlo Mochurad, Liubomyr Shpyrka 🌟
#====================================================
# 🌱 Input Variables for Azure Resources Configuration 🌱
#====================================================
# 🖥️ These variables allow you to customize the deployment of resources on Azure.
# 💡 Ensure to modify them based on your project needs.
#====================================================

# 📦 Resource Group Name
variable "resource_group_name" {
  description = "The name of the resource group"  # 🏷️ Name of the resource group in Azure
  type        = string
  default     = "PDF_recognition"  # 🌍 Default resource group name
}

# 🌍 Location of Resources
variable "location" {
  description = "The Azure region where resources will be created"  # 📍 Region where the resources will be deployed
  type        = string
  default     = "northeurope"  # 🌍 Default location
}

variable "storage-name" {
  description = "Name for storage account"
  type        = string
  default     = "storage4252"
}
