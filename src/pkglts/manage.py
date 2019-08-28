""" Contains functions to manage the structure of the package.

Use 'setup.py' for common tasks.
"""
import logging
from os import listdir, mkdir, remove, walk
from os.path import exists, normpath, splitext
from os.path import join as pj
from shutil import rmtree

from .config import pkg_cfg_file, pkg_hash_file, pkglts_dir
from .config_management import (Config, DEFAULT_CFG,
                                get_pkg_config, write_pkg_config)
from .hash_management import (get_pkg_hash, modified_file_hash,
                              pth_as_key, write_pkg_hash)
from .manage_tools import (check_option_parameters, find_templates,
                           render_template, update_opt)
from .option_tools import available_options, get_user_permission

LOGGER = logging.getLogger(__name__)


def init_pkg(rep="."):
    """Initialise a package in given directory.

    Args:
        rep (str): directory to create pkg into, default current

    Returns:
        None
    """
    if not exists(pj(rep, pkglts_dir)):
        mkdir(pj(rep, pkglts_dir))

    LOGGER.info("init package")

    for name in ("regenerate.no", "clean.no"):
        if not exists(pj(rep, pkglts_dir, name)):
            with open(pj(rep, pkglts_dir, name), 'w') as fhw:
                fhw.write("")

    if exists(pj(rep, pkglts_dir, pkg_cfg_file)):
        cfg = get_pkg_config(rep)
    else:
        cfg = Config(DEFAULT_CFG)
    write_pkg_config(cfg, rep)

    if not exists(pj(rep, pkglts_dir, pkg_hash_file)):
        write_pkg_hash({}, rep)


def clean(rep="."):
    """Thorough cleaning of all arborescence rooting at rep.

    Todo: exception list instead of hardcoded one

    Args:
        rep (str): default ".", top directory to clean

    Returns:
        None
    """
    for name in ("build", "dist", "doc/_dvlpt", "doc/build"):
        pth = normpath(pj(rep, name))
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


def add_option(name, cfg):
    """Add a new option to this package.

    Notes: See the list of available options online

    Args:
        name (str): name of option to add
        cfg (Config):  current package configuration

    Returns:
        (Config): updated package configuration
    """
    if name in cfg.installed_options():
        raise UserWarning("option '%s' already included in this package" % name)

    return update_opt(name, cfg)


def install_example_files(option, cfg, target="."):
    """Install example files associated to an option.

    Args:
        option (str): name of option
        cfg (Config):  current package configuration
        target (str): target directory to write into

    Returns:
        (bool): whether operation succeeded or not
    """
    if option not in cfg.installed_options():
        LOGGER.warning("please install option before example files")
        return False

    opt = available_options[option]
    ex_dir = opt.example_dir()
    if ex_dir is None:
        LOGGER.info("option does not provide any example")
        return False

    rg_tree = {}
    find_templates(ex_dir, target, cfg, rg_tree)
    for tgt_pth, src_pths in rg_tree.items():
        render_template(src_pths, tgt_pth, cfg, {})

    return True


def _manage_conflicts(hm_ref, overwrite):
    """Check if files have been modified.

    Args:
        hm_ref (dict): reference hash for blocks
        overwrite (bool): whether or not, by default,
                         overwrite user modified files

    Returns:
        (dict of str, bool): file path, overwrite
    """
    conflicted = []
    for tgt_pth in hm_ref:
        if exists(tgt_pth) and modified_file_hash(tgt_pth, hm_ref):
            conflicted.append(tgt_pth)
        # else file disappeared, regenerate_dir will reload it if managed by pkglts

    overwrite_file = {}
    if conflicted:
        if overwrite:
            for name in conflicted:
                LOGGER.debug("conflicted, '%s'", name)
                overwrite_file[pth_as_key(name)] = True
        else:
            for name in conflicted:
                LOGGER.warning("A non editable section of %s has been modified", name)
                overwrite_file[pth_as_key(name)] = get_user_permission("overwrite", False)

    return overwrite_file


def regenerate_package(cfg, target=".", overwrite=False):
    """Rebuild all automatically generated files.

    Args:
        cfg (Config):  current package configuration
        target (str): target directory to write into
        overwrite (bool): default False, whether or not
                         to overwrite user modified files

    Returns:
        None
    """
    # check consistency of env params
    invalids = []
    for option in cfg.installed_options():
        for name in check_option_parameters(option, cfg):
            invalids.append((option, name))

    if invalids:
        for option, param in invalids:
            LOGGER.warning("param %s is not valid for '%s'", param, option)

        return False

    # check for potential conflicts
    hm_ref = get_pkg_hash(target)
    overwrite_file = _manage_conflicts(hm_ref, overwrite)

    # find template files associated with installed options
    rg_tree = {}
    for name in cfg.installed_options():
        opt = available_options[name]
        resource_dir = opt.resource_dir()
        if resource_dir is None:
            LOGGER.info("option %s does not provide files", name)
        else:
            LOGGER.info("find template for option %s", name)
            find_templates(resource_dir, target, cfg, rg_tree)

    # render all templates
    hmap = {}
    for tgt_pth, src_pths in rg_tree.items():
        loc_map = render_template(src_pths, tgt_pth, cfg, overwrite_file)
        if loc_map is not None:  # non binary file
            hmap[pth_as_key(tgt_pth)] = loc_map

    hm_ref.update(hmap)
    write_pkg_hash(hm_ref, target)


def regenerate_option(cfg, name, target=".", overwrite=False):
    """Call the regenerate function of a given option

    Args:
        cfg (Config):  current package configuration
        name: (str) name of option
        target: (str) target directory to write into
        overwrite (bool): default False, whether or not
                         to overwrite user modified files

    Returns:
        None
    """
    # test existence of option regenerate module
    try:
        opt = available_options[name]
        opt.regenerate(cfg, target, overwrite)
    except KeyError:
        raise KeyError("option '%s' does not exists" % name)
