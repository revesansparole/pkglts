"""Factory to load a specific front end.
"""
from importlib import import_module


def get_install_front_end(name):
    """Load install front end.

    args:
     - name (str): name of front end to load

    return:
     - (module): loaded python module
    """
    try:
        return import_module("pkglts.install_env.%s_front_end" % name)
    except ImportError:
        raise ImportError("Install front end '%s' does not exist" % name)
