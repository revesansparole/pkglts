"""Regroup set of functions that make use of local environment
inside a package. Just a way to normalize pre defined paths.
"""

from os.path import exists

from .file_management import write_file
from .templating import closing_marker, opening_marker


def pkg_full_name(env):
    """Compute name of src dir according to pkgname
    and namespace in environment

    Args:
        env (jinja2.Environment): current working environment

    Returns:
        (str)
    """
    namespace = env.globals['base'].namespace
    if namespace is None:
        return env.globals['base'].pkgname
    else:
        return namespace + "." + env.globals['base'].pkgname


def src_dir(env):
    """Compute name of src dir according to pkgname
    and namespace in environment

    Args:
        env (jinja2.Environment): current working environment

    Returns:
        (str)
    """
    rep = "src"
    namespace = env.globals['base'].namespace
    if namespace is not None:
        rep = rep + "/" + namespace

    pkgname = env.globals['base'].pkgname
    rep = rep + "/" + pkgname

    return rep


namespace_txt = """
# %spkglts,
__import__('pkg_resources').declare_namespace(__name__)
# %s
""" % (opening_marker, closing_marker)


def init_namespace_dir(pth, env):
    """Populate a directory with specific __init__.py
    for namespace packages.

    Args:
        pth (str): path in which to create the files

    Returns:
        None
    """
    init_pth = pth + "/__init__.py"
    if not exists(init_pth):
        write_file(init_pth, namespace_txt)
