""" Regroup set of functions that make use of local environment
inside a package. Just a way to normalize pre defined paths.
"""

from importlib import import_module
from os.path import exists

from .file_management import write_file
from .templating import closing_marker, same, opening_marker


def pkg_full_name(pkg_cfg):
    """ Compute name of src dir according to pkgname
    and namespace in info

    Args:
        pkg_cfg (dict of (str: dict)): package config info
    """
    namespace = pkg_cfg['base']['namespace']
    if namespace is None:
        return pkg_cfg['base']['pkgname']
    else:
        return namespace + "." + pkg_cfg['base']['pkgname']


def src_dir(pkg_cfg):
    """ Compute name of src dir according to pkgname
    and namespace in info

    args:
     - pkg_cfg (dict of (str: dict)): package config info
    """
    rep = "src"
    namespace = pkg_cfg['base']['namespace']
    if namespace is not None:
        rep = rep + "/" + namespace

    pkgname = pkg_cfg['base']['pkgname']
    rep = rep + "/" + pkgname

    return rep


def installed_options(pkg_cfg):
    """ Returns a list of installed options according
    to the package config file.

    TODO: sort by dependency
    """
    opts = list(pkg_cfg.keys())

    # handle private non option cfg
    opts = [k for k in opts if not k.startswith("_")]

    return opts


namespace_txt = """
# %spkglts,
__import__('pkg_resources').declare_namespace(__name__)
# %s
""" % (opening_marker, closing_marker)


def init_namespace_dir(pth):
    """ Populate a directory with specific __init__.py
    for namespace packages.

    args:
     - pth (str): path in which to create the files
     - hashmap (dict of (str: str)): map used to store hash of files
    """
    init_pth = pth + "/__init__.py"
    if not exists(init_pth):
        write_file(init_pth, namespace_txt)


def load_handlers(name):
    """ Load handlers associated with a given option

    args:
     - name (str): name of option

    return:
     - (dict of (str: func))
    """
    handlers = {name: same}
    # find definition file
    try:
        opt_handlers = import_module("pkglts.option.%s.handlers" % name)
    except ImportError:
        raise KeyError("option '%s' does not exists" % name)

    handlers.update(opt_handlers.mapping)

    return handlers


def load_all_handlers(pkg_cfg):
    """ Load handlers for installed options

    args:
     - pkg_cfg (dict of (str: dict)): package config
    """
    handlers = {}
    for name in installed_options(pkg_cfg):
        handlers.update(load_handlers(name))

    return handlers
