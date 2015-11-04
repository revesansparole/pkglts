# {{pkglts version,
#  -*- coding: utf-8 -*-

major = {{key, version.major}}
minor = {{key, version.minor}}
post = {{key, version.post}}

__version__ = ".".join([str(s) for s in (major, minor, post)])
# }}
