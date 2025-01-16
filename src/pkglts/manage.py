""" Contains functions to manage the structure of the package.

Use 'setup.py' for common tasks.
"""

import logging
from pathlib import Path
from shutil import rmtree

from .config import pkg_hash_file, pkglts_dir
from .config_management import Config, DEFAULT_CFG, get_pkg_config, write_pkg_config
from .hash_management import get_pkg_hash, modified_file_hash, pth_as_key, write_pkg_hash
from .manage_tools import check_option_parameters, find_templates, render_template, update_opt
from .option_tools import available_options, get_user_permission
from .small_tools import ensure_created

LOGGER = logging.getLogger(__name__)


def init_pkg(rep="."):
    """Initialise a package in given directory.

    Args:
        rep (Path): directory to create pkg into, default current

    Returns:
        None
    """
    loc_pkglts_dir = rep / pkglts_dir
    ensure_created(loc_pkglts_dir)

    LOGGER.info("init package")

    for name in ("regenerate.no", "clean.no"):
        (loc_pkglts_dir / name).touch()

    try:
        cfg = get_pkg_config(rep)
    except FileNotFoundError:
        cfg = Config(DEFAULT_CFG)
    write_pkg_config(cfg, rep)

    if not (loc_pkglts_dir / pkg_hash_file).exists():
        write_pkg_hash({}, rep)


def clean(rep="."):
    """Thorough cleaning of all arborescence rooting at rep.

    Todo: exception list instead of hardcoded one

    Args:
        rep (Path): default ".", top directory to clean

    Returns:
        None
    """
    root_dir = Path(rep)
    try:
        cfg = get_pkg_config(rep)

        try:
            doc_dir = root_dir / cfg["sphinx"]["doc_dir"]
            for pth in (doc_dir / "build", doc_dir / "_dvlpt"):
                if pth.exists():
                    rmtree(pth)
        except KeyError:
            pass
    except FileNotFoundError:
        pass

    for name in ("build", "dist"):
        pth = root_dir / name
        if pth.exists():
            rmtree(pth)

    for dir_pth in tuple(root_dir.glob("**/")):
        if dir_pth.exists():  # could have been removed with a previous rmtree
            if not dir_pth.name.startswith(".") and len(tuple(dir_pth.glob("clean.no"))) == 0:
                if dir_pth.name == "__pycache__":
                    rmtree(dir_pth)
                else:
                    for pth in dir_pth.glob("*.pyc"):
                        if not pth.name.startswith("."):
                            pth.unlink()
                    for pth in dir_pth.glob("*.pyo"):
                        if not pth.name.startswith("."):
                            pth.unlink()


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
        raise UserWarning(f"option '{name}' already included in this package")

    return update_opt(name, cfg)


def install_example_files(option, cfg, target=Path(".")):
    """Install example files associated to an option.

    Args:
        option (str): name of option
        cfg (Config):  current package configuration
        target (Path): target directory to write into

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
    for tgt_key, src_pths in rg_tree.items():
        render_template(src_pths, Path(tgt_key), cfg, {})

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
    for tgt_key in hm_ref:
        tgt_pth = Path(tgt_key)
        if tgt_pth.exists() and modified_file_hash(tgt_pth, hm_ref):
            conflicted.append(tgt_pth)
        # else file disappeared, regenerate_dir will reload it if managed by pkglts

    overwrite_file = {}
    if conflicted:
        if overwrite:
            for pth in conflicted:
                LOGGER.debug("conflicted, '%s'", pth)
                overwrite_file[pth_as_key(pth)] = True
        else:
            for pth in conflicted:
                LOGGER.warning("A non editable section of %s has been modified", pth)
                overwrite_file[pth_as_key(pth)] = get_user_permission("overwrite", False)

    return overwrite_file


def regenerate_package(cfg, target=Path("."), overwrite=False):
    """Rebuild all automatically generated files.

    Args:
        cfg (Config):  current package configuration
        target (Path): target directory to write into
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
    for name in cfg.installed_options(return_sorted=True):
        opt = available_options[name]
        resource_dir = opt.resource_dir()
        if resource_dir is None:
            LOGGER.info("option %s does not provide files", name)
        else:
            LOGGER.info("find template for option %s", name)
            find_templates(resource_dir, target, cfg, rg_tree)

    # render all templates
    hmap = {}
    for tgt_key, src_pths in rg_tree.items():
        loc_map = render_template(src_pths, Path(tgt_key), cfg, overwrite_file)
        if loc_map is not None:  # non binary file
            hmap[tgt_key] = loc_map

    hm_ref.update(hmap)
    write_pkg_hash(hm_ref, target)


def regenerate_option(cfg, name, target=".", overwrite=False):
    """Call the regenerate function of a given option

    Args:
        cfg (Config):  current package configuration
        name: (str) name of option
        target: (Path) target directory to write into
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
        raise KeyError(f"option '{name}' does not exists")


def reset_package(cfg, target=Path(".")):
    """Remove all templated files from packages.

    Args:
        cfg (Config):  current package configuration
        target: (Path) target directory to write into

    Returns:
        None
    """
    hm_ref = get_pkg_hash(target)

    # remove all templates
    for tgt_pth in list(hm_ref):
        LOGGER.debug("remove file '%s'", tgt_pth)
        try:
            Path(tgt_pth).unlink()
        except FileNotFoundError:
            LOGGER.debug("File '%s' does not exist", tgt_pth)

        del hm_ref[tgt_pth]

    write_pkg_hash(hm_ref, target)
