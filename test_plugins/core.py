

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def _not_in(item, collection):
	return item not in collection

def _contains(collection, item):
	return item in collection

def _not_contains(collection, item):
	return item not in collection


class TestModule(object):
	"""
	Ansible test module
	"""

	def tests(self):
		return {
			"contains": _contains,
			"not_in": _not_in,
			"not_contains": _not_contains,
		}


