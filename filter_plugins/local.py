

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.six import PY3, iteritems, string_types
from ansible.module_utils.six.moves.urllib.parse import quote, quote_plus, unquote_plus
from ansible.module_utils._text import to_bytes, to_text


def _defaultattr(data, attr, default=None):
	if isinstance(data, dict) == False:
		raise TypeError("data should be a dict")
	elif attr in data:
		return data
	else:
		result = dict()
		result.update(data)
		result.setdefault(attr, default)
		return result
		

class FilterModule(object):
	"""
	Ansible filter module
	"""

	def filters(self):
		return {
			"defaultattr": _defaultattr
		}


