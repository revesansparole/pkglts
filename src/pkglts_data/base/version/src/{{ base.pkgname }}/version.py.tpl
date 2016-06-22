# {# pkglts, version
#  -*- coding: utf-8 -*-

major = {{ version.major }}
minor = {{ version.minor }}
post = {{ version.post }}

__version__ = ".".join([str(s) for s in (major, minor, post)])
# #}
