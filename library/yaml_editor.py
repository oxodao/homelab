#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
import os
import json
import yaml
__metaclass__ = type


from ansible.module_utils.basic import AnsibleModule

# https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html
# This is a simple module that takes a filename
# Load it in yaml
# Replace the key with the given value


def run_module():
    module_args = dict(
        action=dict(type='str', required=True),
        filename=dict(type='str', required=True),
        key=dict(type='str', required=True),
        value=dict(type='dict', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    data = {}
    if os.path.exists(module.params['filename']):
        with open(module.params['filename'], 'r') as f:
            data = yaml.safe_load(f)

    if module.params.get('action', 'set') == 'set':
        # data[module.params['key']] = json.loads(module.params['value'])
        data[module.params['key']] = module.params['value']
        result['changed'] = True
    elif module.params.get('action', 'set') == 'remove':
        if module.params['key'] in data:
            del data[module.params['key']]

    with open(module.params['filename'], 'w') as f:
        yaml.dump(data, f)


    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()