#====================================================
# 🌟 Authors: Valeriy Manuilyk, Pavlo Mochurad, Liubomyr Shpyrka 🌟
#====================================================
# 🌍 Azure Provider Configuration 🌍
#====================================================
# 🛠️ This block configures the Azure Resource Manager (azurerm) provider.
# 🔑 Make sure the subscription ID corresponds to the correct Azure account.
# ⚡ Features block is left empty, but can be extended for advanced capabilities.
#====================================================

provider "azurerm" {
  features {}  # 🚀 Enables the default features for the azurerm provider
  
  subscription_id = "5c38c4d4-fc47-44d4-a351-139d196a9f4c"  # 🔑 Azure Subscription ID
}
