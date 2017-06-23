"""Regroup set of functions that make use of local environment
inside a package. Just a way to normalize pre defined paths.
"""

from .data_access import get_data_dir
from .templating import render


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


def init_namespace_dir(pth, env):
    """Populate a directory with specific __init__.py
    for namespace packages.

    Args:
        pth (str): path in which to create the files
        env (jinja2.Environment): current working environment

    Returns:
        None
    """
    src_pth = get_data_dir() + "/base/namespace__init__.py.tpl"
    tgt_pth = pth + "/__init__.py"
    render(env, src_pth, tgt_pth)
