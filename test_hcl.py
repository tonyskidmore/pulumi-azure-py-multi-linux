#!/usr/bin/env python3.7

import hcl

with open('variables.tf', 'r') as fp:
    hcl_vars = hcl.load(fp)

print(hcl_vars['variable']['location']['default'])
print(hcl_vars['variable']['resource_group_name']['default'])
