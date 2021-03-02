

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.six import PY3, iteritems, string_types
from ansible.module_utils.six.moves.urllib.parse import quote, quote_plus, unquote_plus
from ansible.module_utils._text import to_bytes, to_text


def _pciaddr(data, format="pciutils"):
	domain = 0
	bus = int(data["bus"], 16)
	device = int(data["device"], 16)
	function = int(data["function"], 16)

	if "domain" in data:
		domain = int(data["domain"], 16)

	if format != "xorg":
		return "%04x:%02x:%02x.%1x" % (domain, bus, device, function)
	elif domain != 0:
		return "%d@%d:%d:%d" % (bus, domain, device, function)
	else:
		return "%d:%d:%d" % (bus, device, function)


class FilterModule(object):
	"""
	Ansible filter module
	"""

	def filters(self):
		return {
			"pciaddr": _pciaddr
		}


