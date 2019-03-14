"""
Maintain version for this package.
"""
# {# pkglts, version
#  -*- coding: utf-8 -*-

MAJOR = 4
"""(int) Version major component."""

MINOR = 6
"""(int) Version minor component."""

POST = 1
"""(int) Version post or bugfix component."""

__version__ = ".".join([str(s) for s in (MAJOR, MINOR, POST)])
# #}
