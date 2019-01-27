#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import tempfile

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import b
from ansible.module_utils._text import to_bytes, to_native

#
# Classes representing elements of kernel command line
#

class Flag(object):
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return 'Flag(%s)' % self.name

	def to_text(self):
		return self.name

class Option(object):
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def __repr__(self):
		return 'Option(%s=%s)' % (self.name, self.value)

	def to_text(self):
		return self.name + b('=') + self.value

#
# Functions to parse kernel command line
#

flag_pattern = re.compile(b('\S+'))
option_pattern = re.compile(b('(\S+)=(\S+)'))
separator_pattern = re.compile(b('\s+'))

def parse(cmdline):
	chunks = cmdline.split()
	output = []
	for chunk in chunks:
		if '=' in chunk:
			temp = chunk.split('=', 2)
			output.append(Option(temp[0], temp[1]))
		elif chunk != '':
			output.append(Flag(chunk))
	return output

#
# Functions to serialize kernel command line
#

def serialize(cmdline):
	return b(' ').join([ part.to_text() for part in cmdline ])

#
# Main Module Code
#

def main():
	module = AnsibleModule(
		argument_spec=dict(
			dest=dict(required=True, aliases=['name', 'destfile'], type='path'),
			region=dict(required=True),
			target=dict(required=True, choices=['flag', 'option', 'item']),
			state=dict(required=True, choices=['present', 'absent']),
			flag=dict(default=False, type='str'),
			option=dict(default=False, type='str'),
			value=dict(default=False, type='str'),
			delimiter=dict(default=',', type='str'),
			noempty=dict(default=False, type='bool'),
			backup=dict(default=False, type='bool'),
		),
		add_file_common_args=True,
		supports_check_mode=True,
	)

	params = module.params
	dest = params['dest']
	region = params['region']
	target = params['target']
	state = params['state']
	flag = params['flag']
	option = params['option']
	value = params['value']
	delimiter = params['delimiter']
	noempty = params['noempty']
	backup = params['backup']

	changed = False
	message = ''
	backupfile = ''
	differences = []
	debug = {}

	b_dest = to_bytes(dest, errors='surrogate_or_strict')
	b_region = to_bytes(region, errors='surrogate_or_strict')
	b_oldcontent = b('')
	b_newcontent = b('')

	matcher = re.compile(b_region, re.MULTILINE)

	if not os.path.exists(b_dest):
		module.fail_json(rc=257, msg='Destination %s does not exist' % dest)
	elif os.path.isdir(b_dest):
		module.fail_json(rc=257, msg='Destination %s is a directory' % dest)
	elif target == 'flag' and flag == False:
		module.fail_json(rc=256, msg='Flag is not specified when updating flag')
	elif target == 'option' and option == False:
		module.fail_json(rc=256, msg='Option is not specified when updating option')
	elif target == 'option' and state == 'present' and value == False:
		module.fail_json(rc=256, msg='Value is not specified when setting option')
	elif target == 'item' and option == False:
		module.fail_json(rc=256, msg='Option is not specified when updating option')
	elif target == 'item' and value == False:
		module.fail_json(rc=256, msg='Value is not specified when setting option item')
	elif flag != False and ' ' in flag:
		module.fail_json(rc=256, msg='Flag cannot contain space')
	elif option != False and ' ' in option:
		module.fail_json(rc=256, msg='Option cannot contain space')
	elif value != False and ' ' in value:
		module.fail_json(rc=256, msg='Value cannot contain space')
	elif ' ' in delimiter:
		module.fail_json(rc=256, msg='Delimiter cannot contain space')
	elif matcher.groups < 1:
		module.fail_json(rc=258, msg='Region %s does not contain any group' % region)

	with open(b_dest, 'rb') as f:
		b_oldcontent = b('').join(f.readlines())
		b_newcontent = b_oldcontent
		match = matcher.search(b_oldcontent)

		if match != None:
			if match.start(1) == -1:
				module.fail_json(rc=258, msg='Region %s does not indicate the location of the kernel command line' % region)
			elif match.end(1) == -1:
				module.fail_json(rc=258, msg='Region %s does not indicate the location of the kernel command line' % region)
	
			b_oldline = match.group(1)
			b_newline = b_oldline
			operation = ''
	
			if target == 'flag' and state == 'present':
				operation = 'Flag %s is inserted to kernel command line in file %s' % (flag, dest)
				b_newline = insert_flag(b_oldline, flag)
			elif target == 'flag' and state == 'absent':
				operation = 'Flag %s is removed from kernel command line in file %s' % (flag, dest)
				b_newline = remove_flag(b_oldline, flag)
			elif target == 'option' and state == 'present':
				operation = 'Option %s is updated to "%s" for kernel command line in file %s' % (option, value, dest)
				b_newline = insert_option(b_oldline, option, value)
			elif target == 'option' and state == 'absent':
				operation = 'Option %s is removed from kernel command line in file %s' % (option, dest)
				b_newline = remove_option(b_oldline, option)
			elif target == 'item' and state == 'present':
				operation = 'Option %s is updated to include "%s" for kernel command line in file %s' % (option, value, dest)
				b_newline = insert_option_item(b_oldline, option, delimiter, value)
			elif target == 'item' and state == 'absent':
				operation = 'Option %s is updated to exclude "%s" for kernel command line in file %s' % (option, value, dest)
				b_newline = remove_option_item(b_oldline, option, delimiter, value, noempty)

			debug['oldline'] = to_native(b_oldline)
			debug['newline'] = to_native(b_newline)
			debug['parsed_oldline'] = repr(parse(b_oldline))
			debug['parsed_newline'] = repr(parse(b_newline))

			if b_oldline != b_newline:
				b_newcontent = b_oldcontent[:match.start(1)] + b_newline + b_oldcontent[match.end(1):]
				changed = True
				message = operation

				if module._diff:
					delta = {}
					delta['before_header'] = '%s (content)' % dest
					delta['after_header'] = '%s (content)' % dest
					delta['before'] = to_native(b_oldcontent)
					delta['after'] = to_native(b_newcontent)
					differences.append(delta)
				
	if changed and not module.check_mode:
		if backup:
			backupfile = module.backup_local(dest)

		tmpfd, tmppath = tempfile.mkstemp()
		tmpfile = os.fdopen(tmpfd, 'wb')
		tmpfile.write(b_newcontent)
		tmpfile.close()
		
		module.atomic_move(
			tmppath,
			to_native(os.path.realpath(b_dest), errors='surrogate_or_strict'),
			unsafe_writes=module.params['unsafe_writes']
		)

	stats = module.load_file_common_arguments(params)
	delta = {}

	if module.set_fs_attributes_if_different(stats, False, diff = delta):
		changed = True
		message += " and stats of the file is also changed"

		if module._diff:
			delta['before_header'] = '%s (file attributes)' % dest
			delta['after_header'] = '%s (file attributes)' % dest
			differences.append(delta)

	module.exit_json(
		changed=changed,
		msg=message,
		backup_file=backupfile,
		diff=differences,
		debug=debug
	)

def insert_flag(line, flag):
	parts = parse(line)
	target = next((part for part in parts if isinstance(part, Flag) and part.name == flag), None)
	return serialize(parts + [ Flag(flag) ]) if target == None else line

def remove_flag(line, flag):
	parts = parse(line)
	target = next((part for part in parts if isinstance(part, Flag) and part.name == flag), None)
	return serialize([ part for part in parts if part != target ]) if target != None else line
	
def insert_option(line, option, value):
	parts = parse(line)
	target = next((part for part in parts if isinstance(part, Option) and part.name == option), None)

	if target == None:
		return serialize(parts + [ Option(option, value) ])
	elif target.value != value:
		target.value = value
		return serialize(parts)
	else:
		return line

def remove_option(line, option):
	parts = parse(line)
	target = next((part for part in parts if isinstance(part, Option) and part.name == option), None)
	return serialize([ part for part in parts if part != target ]) if target != None else line

def insert_option_item(line, option, delimiter, value):
	parts = parse(line)
	target = next((part for part in parts if isinstance(part, Option) and part.name == option), None)

	if target == None:
		return serialize(parts + [ Option(option, value) ])
	elif target.value == "":
		target.value = value
		return serialize(parts)
	elif value not in target.value.split(delimiter):
		target.value += delimiter
		target.value += value
		return serialize(parts)
	else:
		return line

def remove_option_item(line, option, delimiter, value, noempty=False):
	parts = parse(line)
	target = next((part for part in parts if isinstance(part, Option) and part.name == option), None)

	if target == None:
		return line
	elif target.value == "" and noempty == False:
		return line
	elif target.value == "" and noempty == True:
		return serialize(part for part in parts if part != target)

	items = option.value.split(delimiter)
	count = len(items)

	if value not in items:
		return line
	elif count == 1:
		return serialize(part for part in parts if part != target)
	else:
		option.value = delimiter.join([ item for item in items if item != value ])
		return serialize(parts)

#
# Run the main module code if launched directly
#

if __name__ == '__main__':
	main()


