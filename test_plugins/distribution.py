

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.module_utils.six import PY3, string_types
from distutils.version import LooseVersion, StrictVersion


_family_map = {
	"ubuntu": [ "debian", "ubuntu" ],
	"mint":   [ "debian", "ubuntu" ],
	"centos": [ "redhat" ],
}

_version_map = {
	"debian": {
		"buzz"       : "1.1",        "rex"        : "1.2",        "bo"         : "1.3",
		"hamm"       : "2.0",        "slink"      : "2.1",        "potato"     : "2.2",
		"woody"      : "3.0",        "sarge"      : "3.1",        "etch"       : "4.0",
		"lenny"      : "5.0",        "squeeze"    : "6.0",        "wheezy"     : "7.0",
		"jessie"     : "8.0",        "stretch"    : "9.0",        "buster"     : "10.0",
	},

	"ubuntu": {
		"warty"      : "4.10",       "hoary"      : "5.04",       "breezy"     : "5.10",
		"dapper"     : "6.06",       "edgy"       : "6.10",       "feisty"     : "7.04",
		"gusty"      : "7.10",       "hardy"      : "8.04",       "interpid"   : "8.10",
		"jaunty"     : "9.04",       "karmic"     : "9.10",       "lucid"      : "10.04",
		"maverick"   : "10.10",      "natty"      : "11.04",      "oneiric"    : "11.10",
		"precise"    : "12.04",      "quantal"    : "12.10",      "raring"     : "13.04",
		"saucy"      : "13.10",      "trusty"     : "14.04",      "utopic"     : "14.10",
		"vivid"      : "15.04",      "wily"       : "15.10",      "xenial"     : "16.04",
		"yakkety"    : "16.10",      "zesty"      : "17.04",      "artful"     : "17.10",
		"bionic"     : "18.04",      "cosmic"     : "18.10",      "disco"      : "19.04",
	},
}


def _version(distribution, version, strict=False):
	Version = StrictVersion if strict else LooseVersion
	output = Version(str(version))
	if distribution in _version_map:
		if version in _version_map[distribution]:
			output = Version(str(_version_map[distribution][version]))
	return output


def _distribution(data, name, release, attribute=None, strict=False):
	if isinstance(data, dict) == False:
		raise TypeError("data should be a dict")
	elif isinstance(name, string_types) == False:
		raise TypeError("name should be a str")
	elif isinstance(release, string_types) == False:
		raise TypeError("release should be a str")
	elif isinstance(strict, bool) == False:
		raise TypeError("strict should be a bool")

	if attribute == None:
		attribute = "criteria"
		criteria = data
	else:
		if isinstance(attribute, string_types) == False:
			raise TypeError("attribute should be a str if provided")
		elif attribute not in data:
			return True
		elif data[attribute] == None:
			return True
		else:
			criteria = data[attribute]

	if isinstance(criteria, dict) == False:
		raise TypeError("%s should be a dict" % attribute)
	elif "family" in criteria and isinstance(criteria["family"], string_types) == False:
		raise TypeError("family should be a str when it appears in %s" % attribure)
	elif "distribution" in criteria and isinstance(criteria["distribution"], string_types) == False:
		raise TypeError("distribution should be a str when it appears in %s" % attribute)
	elif "version" in criteria and isinstance(criteria["version"], string_types) == False:
		raise TypeError("version should be a str when it appears in %s" % attribute)
	elif "since" in criteria and isinstance(criteria["since"], string_types) == False:
		raise TypeError("since should be a str when it appears in %s" % attribute)
	elif "until" in criteria and isinstance(criteria["until"], string_types) == False:
		raise TypeError("until should be a str when it appears in %s" % attribute)
	elif "distribution" not in criteria and "version" in criteria:
		raise ValueError("version cannot appear in %s without distribution" % attribute)
	elif "distribution" not in criteria and "since" in criteria:
		raise ValueError("since cannot appear in %s without distribution" % attribute)
	elif "distribution" not in criteria and "until" in criteria:
		raise ValueError("until cannot appear in %s without distribution" % attribute)
	elif "version" in criteria and "since" in criteria:
		raise ValueError("version cannot appear together with since in %s" % attribute)
	elif "version" in criteria and "until" in criteria:
		raise ValueError("version cannot appear together with until in %s" % attribute)

	distribution = name.lower()
	version = _version(distribution, release)
	families = _family_map[distribution] if distribution in _family_map else [ distribution ]

	if "family" in criteria and criteria["family"] not in families:
		return False
	elif "distribution" in criteria and criteria["distribution"] != distribution:
		return False
	elif "version" in criteria and _version(distribution, criteria["version"]) != version:
		return False
	elif "since" in criteria and _version(distribution, criteria["since"]) > version:
		return False
	elif "until" in criteria and _version(distribution, criteria["until"]) < version:
		return False
	else:
		return True


class TestModule(object):
	"""
	Ansible test module for dealing with linux distributions.
	"""

	def tests(self):
		return {
			"distribution": _distribution,
		}


