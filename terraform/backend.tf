terraform {
  backend "azurerm" {
    resource_group_name  = "backendresourcegroup777"
    storage_account_name = "tfstateaccount4245"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
