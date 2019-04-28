variable "resource_group_name" {
  description = "The name of the resource group"
  default = "build-123"
}

variable "rg_prefix" {
  description = "The shortened abbreviation to represent your resource group that will go on the front of some resources."
  default     = "rg"
}

variable "nsg_source_address_prefix" {
  description = "CIDR source prefix for network security group."
  default     = "*"
}

variable "location" {
  description = "The location/region where the resource group is created. Changing this forces a new resource to be created."
  default = "uksouth"
}

variable "ssh_key_data" {
    description = "Public SSH key to be used for passwordless SSH access"
}


variable "admin_username" {
  description = "Admin username"
  default     = "cloud_admin"
}
variable "admin_password" {
  description = "Admin password"
  default     = "Testing123"
}

variable "network_name" {
  description = "network name"
  default     = "server-network"
}

variable "network_address_spaces" {
  description = "VNET address space"
  default     = ["10.0.0.0/16"]
}

variable "network_subnets" {
  description = "VNET subnets"
  default     = [{
        name            = "default"
        address_prefix  = "10.0.1.0/24"
    }]
}

variable "network_additional_subnet_name" {
  description = "Additional network subnet name"
  default     = "server-subnet"
}

variable "network_additional_subnet_address_prefix" {
  description = "Additional network subnet address prefix"
  default     = "10.0.2.0/24"
}

variable "network_public_ip_name" {
  description = "Name of public IP address"
  default     = "server-ip"
}

variable "network_public_ip_allocation_method" {
  description = "Public IP address allocation method"
  default     = "Dynamic"
}

variable "virtual_machines" {
  description = "Virtual Machines to create"
  default     = [
    {
        name            = "jump"
        publisher       = "OpenLogic"
        offer           = "CentOS"
        sku             = "7.6"
        version         = "latest"
    },
    {
        name            = "CentOS7"
        publisher       = "OpenLogic"
        offer           = "CentOS"
        sku             = "7.6"
        version         = "latest"
    },
    {
        name            = "CentOS6"
        publisher       = "OpenLogic"
        offer           = "CentOS"
        sku             = "6.10"
        version         = "latest"
    }
  ]
}

