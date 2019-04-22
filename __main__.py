#!/usr/bin/env python3.7

import pulumi
from pulumi import Output
from pulumi_azure import core, compute, network
import hcl

config = pulumi.Config("azure-web")
username = config.require("username")
password = config.require("password")

with open('variables.tf', 'r') as fp:
    hcl_vars = hcl.load(fp)

resource_group = core.ResourceGroup(
               hcl_vars['variable']['resource_group_name']['default'],
               name=hcl_vars['variable']['resource_group_name']['default'],
               location=hcl_vars['variable']['location']['default'])


net = network.VirtualNetwork(
    hcl_vars['variable']['network_name']['default'],
    name=hcl_vars['variable']['network_name']['default'],
    resource_group_name=resource_group.name,
    location=resource_group.location,
    address_spaces=hcl_vars['variable']['network_address_spaces']['default'],
    subnets=hcl_vars['variable']['network_subnets']['default']
)

subnet = network.Subnet(
    hcl_vars['variable']['network_additional_subnet_name']['default'],
    name=hcl_vars['variable']['network_additional_subnet_name']['default'],
    resource_group_name=resource_group.name,
    virtual_network_name=net.name,
    address_prefix=hcl_vars['variable']['network_additional_subnet_address_prefix']['default'])

public_ip = network.PublicIp(
    hcl_vars['variable']['network_public_ip_name']['default'],
    name=hcl_vars['variable']['network_public_ip_name']['default'],
    resource_group_name=resource_group.name,
    location=resource_group.location,
    allocation_method=hcl_vars['variable']['network_public_ip_allocation_method']['default'])

network_iface = network.NetworkInterface(
    "server-nic",
    name="server-nic",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    ip_configurations=[{
        "name": "webserveripcfg",
        "subnet_id": subnet.id,
        "private_ip_address_allocation": "Dynamic",
        "public_ip_address_id": public_ip.id,
    }])

userdata = """#!/bin/bash

echo "Hello, World!" > index.html
nohup python -m SimpleHTTPServer 80 &"""

vm = compute.VirtualMachine(
    "server-vm",
    name="server-vm",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    network_interface_ids=[network_iface.id],
    vm_size="Standard_A0",
    delete_data_disks_on_termination=True,
    delete_os_disk_on_termination=True,
    os_profile={
        "computer_name": "hostname",
        "admin_username": username,
        "admin_password": password,
        "custom_data": userdata,
    },
    os_profile_linux_config={
        "disable_password_authentication": False,
    },
    storage_os_disk={
        "create_option": "FromImage",
        "name": "myosdisk1",
    },
    storage_image_reference={
        "publisher": "canonical",
        "offer": "UbuntuServer",
        "sku": "16.04-LTS",
        "version": "latest",
    })

combined_output = Output.all(vm.id, public_ip.name,
                             public_ip.resource_group_name)
public_ip_addr = combined_output.apply(
    lambda lst: network.get_public_ip(name=lst[1], resource_group_name=lst[2]))
pulumi.export("public_ip", public_ip_addr.ip_address)
