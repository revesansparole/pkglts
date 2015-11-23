# rev = 1
""" Contains functions to manage the structure of the package.

Use 'setup.py' for common tasks.
"""

import json
import logging
from os import listdir, mkdir, remove, walk
from os.path import exists, splitext
from os.path import join as pj
from shutil import rmtree

from .local import load_all_handlers, installed_options
from .manage_tools import (check_option_parameters, package_hash_keys,
                           clone_base_option, clone_example, regenerate_pkg,
                           update_opt)
from .option_tools import get_user_permission
from .rmtfile import ls
from .templating import replace
from .versioning import get_github_version, get_local_version


try:
    string_type = basestring
except NameError:
    string_type = str

logger = logging.getLogger(__name__)

pkglts_dir = ".pkglts"
pkg_cfg_file = "pkg_cfg.json"
pkg_hash_file = "pkg_hash.json"


class FormattedString(str):
    """Small class to hold both formatted string and its template
    """
    pass


def init_pkg(rep="."):
    """ Initialise a package in given directory
    """
    if not exists(pj(rep, pkglts_dir)):
        mkdir(pj(rep, pkglts_dir))

    for name in ("regenerate.no", "clean.no"):
        if not exists(pj(pkglts_dir, name)):
            with open(pj(pkglts_dir, name), 'w') as f:
                f.write("")

    if exists(pj(rep, pkglts_dir, pkg_cfg_file)):
        pkg_cfg = get_pkg_config(rep)
    else:
        pkg_cfg = {}
    if '_pkglts' not in pkg_cfg:
        pkg_cfg['_pkglts'] = dict(use_prompts=False,
                                  auto_install=True)
    write_pkg_config(pkg_cfg, rep)

    if not exists(pj(rep, pkglts_dir, pkg_hash_file)):
        write_pkg_hash({}, rep)


def get_pkg_config(rep="."):
    """ Read pkg_cfg file associated to this package

    args:
     - rep (str): directory to search for info

    return:
     - (dict of (str, dict)): option_name: options
    """
    with open(pj(rep, pkglts_dir, pkg_cfg_file), 'r') as f:
        pkg_cfg = json.load(f)

    # format template entries
    handlers = {}  # use only default handlers
    for name, cfg in tuple(pkg_cfg.items()):
        for key, param in tuple(cfg.items()):
            if isinstance(param, string_type):
                new_value = replace(param, handlers, pkg_cfg)
                if new_value == param:
                    cfg[key] = param
                else:
                    cfg[key] = FormattedString(new_value)
                    cfg[key].template = param

    return pkg_cfg


def write_pkg_config(pkg_cfg, rep="."):
    """ Store config associated to this package on disk

    args:
     - pkg_cfg (dict of (str, dict)): option_name, options
     - rep (str): directory to search for info
    """
    logger.info("write package config")
    cfg = dict(pkg_cfg)
    for name, params in tuple(cfg.items()):
        for key, param in tuple(params.items()):
            if isinstance(param, FormattedString):
                params[key] = param.template

    with open(pj(rep, pkglts_dir, pkg_cfg_file), 'w') as f:
        json.dump(cfg, f, sort_keys=True, indent=4)


def get_pkg_hash(rep="."):
    """ Read pkg_hash file associated to this package

    args:
     - rep (str): directory to search for info

    return:
     - (dict of (str, hash)): file path: hash key
    """
    with open(pj(rep, pkglts_dir, pkg_hash_file), 'r') as f:
        hm = json.load(f)

    return dict((pth, tuple(key)) for pth, key in hm.items())


def write_pkg_hash(pkg_hash, rep="."):
    """ Store hash associated to this package on disk

    args:
     - pkg_hash (dict of (str, hash)): file path: hash key
     - rep (str): directory to search for info
    """
    logger.info("write package hash")
    cfg = dict(pkg_hash)

    with open(pj(rep, pkglts_dir, pkg_hash_file), 'w') as f:
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
        for name in tuple(dnames):
            if "clean.no" in listdir(pj(root, name)):
                dnames.remove(name)
            elif name.startswith("."):
                dnames.remove(name)
            elif name == "__pycache__":
                rmtree(pj(root, name))
                dnames.remove(name)

        for name in fnames:
            if not name.startswith("."):
                if splitext(name)[1] in [".pyc", ".pyo"]:
                    remove(pj(root, name))


def update_pkg(pkg_cfg):
    """ Check if a new version of ltspkg exists
    """
    gth_ver = get_github_version()
    if gth_ver is None:
        print("Unable to fetch current github version")
        return pkg_cfg

    loc_ver = get_local_version()
    if gth_ver <= loc_ver:
        logger.info("package is up to date, nothing to do")
    else:
        logger.info("newer version of package available")
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

    return update_opt(name, pkg_cfg)


def edit_option(name, pkg_cfg):
    """ Edit an already installed option

    args:
     - name (str): name of option to update
     - pkg_cfg (dict of (str, dict)): option_name, options
    """
    if name not in pkg_cfg:
        raise UserWarning("Option '%s' seems not to be installed" % name)

    print("edit pkg_cfg.json file by hand instead")
    return pkg_cfg
    # return update_opt(name, pkg_cfg)


def add_option(name, pkg_cfg):
    """ Add a new option to this package.
    See the list of available option online

    args:
     - name (str): name of option to add
     - pkg_cfg (dict of (str, dict)): package configuration parameters
    """
    if name in pkg_cfg:
        raise UserWarning("option already included in this package")

    return update_opt(name, pkg_cfg)


def install_example_files(option, pkg_cfg, target="."):
    if option not in pkg_cfg:
        logger.warning("please install option before example files")
        return False

    # get handlers
    h = load_all_handlers(pkg_cfg)

    if (option, True) not in ls("pkglts_data/example"):
        logger.info("option does not provide any example")
        return False

    root = "pkglts_data/example/%s" % option
    # walk all files in example repo to copy them handling conflicts on the way
    clone_example(root, target, pkg_cfg, h)


def regenerate(pkg_cfg, target=".", overwrite=False):
    """ Rebuild all automatically generated files

    args:
     - pkg_cfg (dict of (str, dict)): package configuration parameters
     - target (str): target directory to write into
     - overwrite (bool): default False, whether or not
                         to overwrite user modified files
    """
    # check consistency of pkg_cfg
    invalids = []
    for option in installed_options(pkg_cfg):
        invalids.extend(check_option_parameters(option, pkg_cfg))

    if len(invalids) > 0:
        for param in invalids:
            logger.warning("param %s is not valid" % param)

        return False

    # load handlers
    handlers = load_all_handlers(pkg_cfg)

    # check for potential conflicts
    hm_ref = get_pkg_hash(target)

    hm = package_hash_keys(target)
    conflicted = []
    for pth, ref_key in hm_ref.items():
        try:
            key = hm[pth]
            if key != ref_key:
                conflicted.append(pth)
        except KeyError:
            # file disappeared, clone will reload it if managed by pkglts
            pass

    overwrite_file = {}
    if len(conflicted) > 0:
        print("conflicted", conflicted)
        if overwrite:
            for name in conflicted:
                overwrite_file[name] = True
        else:
            for name in conflicted:
                print("A non editable section of %s has been modified" % name)
                overwrite_file[name] = get_user_permission("overwrite", False)

    # copy all missing files for options
    # regenerating pkglts divs on the way
    for option in installed_options(pkg_cfg):
        logger.info("cloning option '%s'" % option)
        error_files = clone_base_option(option, pkg_cfg, handlers, target,
                                        overwrite_file)
        if len(error_files) > 0:
            for pth in error_files:
                logger.warning("unable to resolve conflict in '%s'" % pth)

            return False

    # regenerate files
    # overwrite_file[target + "/pkg_cfg.json"] = False
    # overwrite_file[target + "/pkg_hash.json"] = False
    regenerate_pkg(pkg_cfg, handlers, target, overwrite_file)

    # re create hash
    hm = package_hash_keys(target)
    write_pkg_hash(hm, target)
