

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.six import PY3, iteritems, string_types
from ansible.module_utils.six.moves.urllib.parse import quote, quote_plus, unquote_plus
from ansible.module_utils._text import to_bytes, to_text


class Reducer(object):
	"""
	Reducer combines matching data found in the config tree into the final
	result incrementally.
	"""

	def initial(self):
		pass

	def reduce(self, initial, incoming):
		pass


class SelectReducer(Reducer):
	"""
	SelectReducer combines data by returning the most specific data as the
	final result. Other data are ignored. When there are no matching data,
	then None is returned.
	"""

	def initial(self):
		return None
	
	def reduce(self, initial, incoming):
		if initial == None:
			return incoming
		else:
			return initial


class SumReducer(Reducer):
	"""
	SumReducer combines data by summing them together.
	"""

	def initial(self):
		return 0

	def reduce(self, initial, incoming):
		if isinstance(incoming, int) == False:
			raise TypeError("incoming should be an int")
		else:
			return initial + incoming


class ListReducer(Reducer):
	"""
	ListReducer combines data by placing them into a list. The data will
	appear in the result in decreasing priority. It means that the most
	specific data will appear first, then the second most specific, until
	the most general data in the end.
	"""

	def initial(self):
		return []

	def reduce(self, initial, incoming):
		if isinstance(incoming, str) == False:
			raise TypeError("incoming should be a str")
		else:
			result = list()
			result.extend(initial)
			result.append(incoming)
			return result


class JoinReducer(Reducer):
	"""
	JoinReducer combines data by placing items in the data list into a master
	list. The ordering of items in the list is similar to ListReducer.
	"""

	def initial(self):
		return []

	def reduce(self, initial, incoming):
		if isinstance(incoming, list) == False:
			raise TypeError("incoming should be a list")
		else:
			result = list()
			result.extend(incoming)
			result.extend(initial)
			return result


class MergeReducer(Reducer):
	"""
	MergeReducer combines data by merging entries in the data dict into a
	master dict. The entries from the most specific data dict will override
	entries from the less specific data dict.
	"""

	def initial(self):
		return {}

	def reduce(self, initial, incoming):
		if isinstance(incoming, dict) == False:
			raise TypeError("incoming should be a dict")
		else:
			result = dict()
			result.update(incoming)
			result.update(initial)
			return result


def _walk(tree, selector, attribute, reducer):
	if isinstance(tree, dict) == False:
		raise TypeError("treeconf data should be a dict")

	result = reducer.initial()
	if len(selector) > 0 and selector[0] in tree:
		result = _walk(tree[selector[0]], selector[1:], attribute, reducer)
	if attribute in tree:
		result = reducer.reduce(result, tree[attribute])
	return result


def _treeconf(tree, *args):
	size = len(args)
	last1 = size - 1
	last2 = size - 2

	if args[last1] == "select":
		return _walk(tree, args[:-2], args[last2], SelectReducer())
	elif args[last1] == "sum":
		return _walk(tree, args[:-2], args[last2], SumReducer())
	elif args[last1] == "list":
		return _walk(tree, args[:-2], args[last2], ListReducer())
	elif args[last1] == "join":
		return _walk(tree, args[:-2], args[last2], JoinReducer())
	elif args[last1] == "merge":
		return _walk(tree, args[:-2], args[last2], MergeReducer())
	else:
		raise ValueError("unknown reducer %s" % args[last2])


class FilterModule(object):
	"""
	Ansible filter module
	"""

	def filters(self):
		return {
			"treeconf": _treeconf
		}


