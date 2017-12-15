"""
pkglts helps maintain packages with log term support.
"""
# {# pkglts, base

from . import version

__version__ = version.__version__

# #}

from . import logging_tools

logging_tools.main()
