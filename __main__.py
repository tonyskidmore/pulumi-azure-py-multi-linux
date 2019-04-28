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

# settings for all VMs

admin_username = hcl_vars['variable']['admin_username']['default']
ssh_key_data = hcl_vars['variable']['ssh_key_data']['default']

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

# per VM settings

virtual_machines = hcl_vars['variable']['virtual_machines']['default']
network_ifaces = []
vms = []
vm_counter = 0
vm_size = 'Standard_B1ls'

for virtual_machine in virtual_machines:

    ip_config = [{
            "name": virtual_machine['name'],
            "subnet_id": subnet.id,
            "private_ip_address_allocation": "Dynamic"}]
    if 'public_ip' in virtual_machine and virtual_machine['public_ip'] == "true":
        ip_config[0]['public_ip_address_id'] = public_ip.id

    network_ifaces.append(network.NetworkInterface(
        virtual_machine['name'],
        name=virtual_machine['name'],
        resource_group_name=resource_group.name,
        location=resource_group.location,
        ip_configurations=ip_config)
    )

    vms.append(compute.VirtualMachine(
        virtual_machine['name'],
        name=virtual_machine['name'],
        resource_group_name=resource_group.name,
        location=resource_group.location,
        network_interface_ids=[network_ifaces[vm_counter].id],
        vm_size=vm_size,
        delete_data_disks_on_termination=True,
        delete_os_disk_on_termination=True,
        os_profile={
            "computer_name": "hostname",
            "admin_username": admin_username,
            # "admin_password": password,
            # "custom_data": userdata,
        },
        os_profile_linux_config={
            "disable_password_authentication": True,
            "ssh_keys": [{
                "path": "/home/" + admin_username + "/.ssh/authorized_keys",
                "key_data": ssh_key_data
            }]
        },
        storage_os_disk={
            "create_option": "FromImage",
            "name": virtual_machine['name'],
        },
        storage_image_reference={
            "publisher": virtual_machine['publisher'],
            "offer": virtual_machine['offer'],
            "sku": virtual_machine['sku'],
            "version": virtual_machine['version'],
        })
    )

    vm_counter += 1

combined_output = Output.all(vms[0].id, public_ip.name,
                             public_ip.resource_group_name)
public_ip_addr = combined_output.apply(
    lambda lst: network.get_public_ip(name=lst[1], resource_group_name=lst[2]))
pulumi.export("public_ip", public_ip_addr.ip_address)
