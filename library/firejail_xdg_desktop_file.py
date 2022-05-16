#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: firejail_xdg_desktop_file
short_description: Module to Create Firejail Desktop File from a Source Desktop File

description: >-
  This module parses the source desktop file, updates Exec fields in all sections to
  ensure that the commands are called by firejail, and write the result to the
  the firejail desktop file.

options:
  dest:
    description: Path to the firejail desktop file
    required: true
    type: str
    aliases: [ 'path' ]
  src:
    description: Path to the source desktop file
    required: true
    type: str
  executable:
    description: Path to the firejail executable file
    required: false
    default: firejail
    type: str
  parameters:
    description: Extra command line arguments to firejail
    required: false
    type: str
  validate:
    description: Command to validate the firejail desktop file
    required: false
    type: str
  backup:
    description: Indicates if the original firejail desktop file should be backup
    required: false
    type: bool
'''

EXAMPLES = r'''
- name: "Test Firejail Module"
  firejail_xdg_desktop_file:
    dest: "/home/user/.local/share/applications/steam.desktop"
    src: "/usr/share/applications/steam.desktop"
    parameters: "--join-or-start=steam --profile=steam"
    owner: "user"
    group: "user"
    mode: "0644"
'''

RETURNS = r''' # '''

import os
import re
import tempfile

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import b
from ansible.module_utils._text import to_bytes, to_native

def main():
	module = AnsibleModule(
		argument_spec=dict(
			dest=dict(required=True, aliases=['path'], type='path'),
      src=dict(required=True, type='path'),
			executable=dict(type='str', default='firejail'),
			parameters=dict(type='str', default=''),
			validate=dict(type='str', default=None),
			backup=dict(type='bool', default=False),
		),
		add_file_common_args=True,
		supports_check_mode=True,
	)

	dest = module.params['dest']
	src = module.params['src']
	executable = module.params['executable']
	parameters = module.params['parameters']
	backup = module.params['backup']
	validate = module.params['validate']

	matcher = re.compile(b('^(\s*Exec\s*=\s*)(.*)$'))
	result = dict(changed="", message="")

	b_dest = to_bytes(dest, errors='surrogate_or_strict')
	b_src = to_bytes(src, errors='surrogate_or_strict')
	b_executable = to_bytes(executable, errors='surrogate_or_strict')
	b_parameters = to_bytes(parameters, errors='surrogate_or_strict')
	b_oldcontent = b("")
	b_newcontent = b("")

	if validate != None and "%s" not in validate:
		module.fail_json(msg="validate must contain %%s: %s" % (validate))

	try:
		with open(b_dest, 'rb') as f:
			b_oldcontent = f.read()
	except:
		pass

	try:
		with open(b_src, 'rb') as f:
			for line in f.readlines():
				match = matcher.search(line)
				if match != None:
					b_newcontent += line[:match.end(1)]
					b_newcontent += b_executable
					b_newcontent += b(" ")
					if parameters != '':
						b_newcontent += b_parameters
						b_newcontent += b(" ")
					b_newcontent += line[match.start(2):]
				else:
					b_newcontent += line
	except BaseException as e:
		module.fail_json(msg="cannot read source desktop file %s: %s" % (src, e))

	if b_newcontent != b_oldcontent:
		result['changed'] = True
		result['message'] = "rebuild firejail desktop file %s from original desktop file %s" % (dest, src)

		if not module.check_mode:
			try:
				tmpfd, tmpfile = tempfile.mkstemp(dir=module.tmpdir)

				with os.fdopen(tmpfd, 'wb') as f:
					f.write(b_newcontent)

				if validate != None:
					rc, output, error = module.run_command(to_bytes(validate % tmpfile, errors='surrogate_or_strict'))
					if rc != 0:
						module.fail_json(msg="failed to validate: rc:%s error:%s" % (rc, error))

				if backup == True:
					result["backup_file"] = module.backup_local(dest)

				module.atomic_move(
					tmpfile,
					to_native(os.path.realpath(b_dest), errors='surrogate_or_strict'),
					unsafe_writes=module.params['unsafe_writes']
				)
			except BaseException as e:
				module.fail_json(msg="cannot write firejail desktop file %s: %s" % (dest, e))

	if not module.check_mode:
		stats = module.load_file_common_arguments(module.params)
		changed = module.set_fs_attributes_if_different(stats, False)

		if changed and not result['changed']:
			result['changed'] = True
			result['message'] = "update file stat for firejail desktop file %s" % dest

	module.exit_json(**result)

if __name__ == '__main__':
	main()

