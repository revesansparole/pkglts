# -*- coding: utf-8 -*-
# test {{version.fetch_github rm, {{key, version.auto}}}}

major = {{key, version.major}}
minor = {{key, version.minor}}
post = {{key, version.post}}

__version__ = ".".join([str(s) for s in (major, minor, post)])
