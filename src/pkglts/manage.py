# rev = 1
""" Contains functions to manage the structure of the package.

Use 'setup.py' for common tasks.
"""

import json
from os import remove, walk
from os.path import exists, splitext
from os.path import join as pj
from shutil import rmtree

from .local import load_all_handlers, installed_options
from .manage_tools import check_tempering, regenerate_dir, update_opt
from .option_tools import get_user_permission
from .versioning import get_github_version, get_local_version


def init_pkg(rep="."):
    """ Initialise a package in given directory
    """
    pkg_cfg = {'hash': {}}
    write_pkg_config(pkg_cfg, rep)


def get_pkg_config(rep="."):
    """ Read pkg_cfg file associated to this package

    args:
     - rep (str): directory to search for info

    return:
     - (dict of (str, dict)): option_name: options
    """
    with open(pj(rep, "pkg_cfg.json"), 'r') as f:
        info = json.load(f)

    return info


def write_pkg_config(pkg_cfg, rep="."):
    """ Store config associated to this package on disk

    args:
     - pkg_cfg (dict of (str, dict)): option_name, options
     - rep (str): directory to search for info
    """
    cfg = dict(pkg_cfg)
    for key in tuple(cfg.keys()):
        if key.startswith("_"):
            del cfg[key]

    with open(pj(rep, "pkg_cfg.json"), 'w') as f:
        json.dump(cfg, f, sort_keys=True, indent=4)


def clean(rep="."):
    """ Thorough cleaning of all arborescence rooting at rep.

    # TODO: exception list instead of hardcoded one

    args:
     - rep (str): default ".", top directory to clean
    """
    for name in ("build", "dist"):
        pth = pj(rep, name)
        if exists(pth):
            rmtree(pth)

    for root, dnames, fnames in walk(rep):
        # do not walk directories starting with "."
        for name in list(dnames):
            if name.startswith("."):
                dnames.remove(name)
            if name == "__pycache__":
                rmtree(pj(root, name))
                dnames.remove(name)
            if name == "venv_toto":
                dnames.remove(name)

        for name in fnames:
            if not name.startswith("."):
                if splitext(name)[1] in [".pyc", ".pyo"]:
                    remove(pj(root, name))


def update_pkg(pkg_cfg):
    """ Check if a new version of ltspkg exists
    """
    gth_ver = get_github_version()
    loc_ver = get_local_version()
    if gth_ver <= loc_ver:
        print("package is up to date, nothing to do")
    else:
        print("newer version of package available")
        if get_user_permission("install"):
            print("install")
            # TODO: perform installation
            # if get_user_permission('develop mode'):
            #     print("update your code before continuing")
            #     get_user_permission("continue")
            # else:
            #     pip_args = ['-vvv']
            #     proxy = os.environ['http_proxy']
            #     if proxy:
            #         pip_args.append('--proxy')
            #         pip_args.append(proxy)
            #     pip_args.append('install')
            #     pip_args.append('pkglts')
            #     pip.main(pip_args)
        else:
            return pkg_cfg

        # relaunch config for each installed option
        for opt_name in installed_options(pkg_cfg):
            pkg_cfg = update_option(opt_name, pkg_cfg)

        # regenerate will be called explicitly

    return pkg_cfg


def update_option(name, pkg_cfg):
    """ Update an already installed option

    args:
     - name (str): name of option to update
     - pkg_cfg (dict of (str, dict)): option_name, options
    """
    if name not in pkg_cfg:
        raise UserWarning("Option '%s' seems not to be installed" % name)

    extra = pkg_cfg[name]  # one way to re-force already set args

    return update_opt(name, pkg_cfg, extra)


def edit_option(name, pkg_cfg):
    """ Edit an already installed option

    args:
     - name (str): name of option to update
     - pkg_cfg (dict of (str, dict)): option_name, options
    """
    if name not in pkg_cfg:
        raise UserWarning("Option '%s' seems not to be installed" % name)

    return update_opt(name, pkg_cfg)


def add_option(name, pkg_cfg, extra=None):
    """ Add a new option to this package.
    See the list of available option online

    args:
     - name (str): name of option to add
     - pkg_cfg (dict of (str, dict)): package configuration parameters
     - extra (dict): extra arguments for option configuration
    """
    if name in pkg_cfg:
        raise UserWarning("option already included in this package")

    return update_opt(name, pkg_cfg, extra)


def regenerate(pkg_cfg, target=".", overwrite=False):
    """ Rebuild all automatically generated files

    args:
     - pkg_cfg (dict of (str, dict)): package configuration parameters
     - target (str): target directory to write into
     - overwrite (bool): default False, whether or not
                         to overwrite user modified files
    """
    # parse options and load handlers
    handlers = load_all_handlers(pkg_cfg)

    root = "pkglts_data/base"
    if not overwrite:
        # walk all files in repo to check for possible tempering
        # of files by user
        tf = []
        check_tempering(root, target, handlers, pkg_cfg, tf)
        if len(tf) > 0:
            msg = "These files have been modified by user:\n"
            msg += "\n".join(tf)
            raise UserWarning(msg)

    # walk all files in repo and regenerate them
    regenerate_dir(root, target, handlers, pkg_cfg, True)
