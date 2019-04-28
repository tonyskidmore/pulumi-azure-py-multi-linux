#!/usr/bin/env python3.7

import hcl
# import json

with open('variables.tf', 'r') as fp:
    hcl_vars = hcl.load(fp)

print(hcl_vars['variable']['location']['default'])
print(hcl_vars['variable']['resource_group_name']['default'])

vms = hcl_vars['variable']['virtual_machines']['default']

print(vms[0])

for vm in vms:
    print(vm['name'])


# print("length of array = {}".format(vms))
