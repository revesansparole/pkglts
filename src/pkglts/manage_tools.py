""" Specific helper function for manage script
"""

import logging
from os import listdir, mkdir
from os.path import basename, exists, isdir, splitext

from .hash_management import compute_hash, pth_as_key
from .install_env.load_front_end import get_install_front_end
from .local import init_namespace_dir
from .option_tools import available_options, get_user_permission
from .templating import render

LOGGER = logging.getLogger(__name__)

TPL_SRC_NAME = "{" + "{ base.pkgname }" + "}"

NON_BIN_EXT = ("", ".bat", ".cfg", ".in", ".ini", ".md", ".no", ".ps1", ".py", ".rst", ".sh",
               ".txt", ".yml", ".yaml")


def ensure_installed_packages(requirements, msg, cfg):
    """Ensure all packages in requirements are installed.

    If not, ask user permission to install them.

    Args:
        requirements (list of Dependency): list of package names to install
                                   if needed
        msg (str): error message to print
        cfg (Config):  current package configuration

    Returns:
        (bool): whether all required packages are installed or not
    """
    ife_name = cfg["_pkglts"]['install_front_end']
    req = [dep.name for dep in requirements
           if dep.package_manager is None or dep.package_manager == ife_name]
    ife = get_install_front_end(ife_name)
    to_install = set(req) - set(ife.installed_packages())
    if to_install:
        print(msg)
        LOGGER.warning("missing packages: " + ", ".join(to_install))
        for name in to_install:
            ife.install(name)
            LOGGER.info("install %s", name)

    return True


def check_option_parameters(name, cfg):
    """Check that the parameters associated to an option are valid.

    Try to import Check function in option dir.

    Args:
        name (str): option name
        cfg (Config):  current package configuration
    """
    try:
        opt = available_options[name]
        return opt.check(cfg)
    except KeyError:
        return []


def update_opt(name, cfg):
    """Update an option of this package.

    Notes: If the option does not exists yet, add it first.
           See the list of available option online

    Args:
        name (str): name of option to add
        cfg (Config):  current package configuration
    """
    LOGGER.info("update option %s", name)

    # test existence of option
    try:
        opt = available_options[name]
    except KeyError:
        raise KeyError("option '%s' does not exists" % name)

    # find other option requirements in repository
    for dep in opt.require('option', cfg):
        option_name = dep.name
        if option_name not in cfg.installed_options():
            print("need to install option '%s' first" % option_name)
            if (cfg["_pkglts"]['auto_install'] or
                    get_user_permission("install")):
                cfg = update_opt(option_name, cfg)
            else:
                return cfg

    # find extra package requirements for setup
    msg = "this option requires some packages to setup"
    if not ensure_installed_packages(opt.require('setup', cfg), msg, cfg):
        print("option installation stopped")
        return cfg

    # find parameters required by option config
    opt.update_parameters(cfg.template())
    cfg.resolve()

    # find extra package requirements for dvlpt
    msg = "this option requires additional packages for developers"
    ensure_installed_packages(opt.require('dvlpt', cfg), msg, cfg)

    return cfg


def _rg_dir(src_pth, tgt_name, tgt_pth, cfg, overwrite_file):
    """Regenerate a directory.

    Notes:
        recursively regenerate all tree rooted on src_pth

    Args:
        src_pth (str): path to directory
        tgt_name (str): name of directory to create
        tgt_pth (str): path to created directory
        cfg (Config):  current package configuration
        overwrite_file (dict): which files to overwrite

    Returns:
        (dict of str, map): hash key of preserved sections
    """
    if tgt_name in ("", "_"):
        return {}

    if not exists(tgt_pth):
        mkdir(tgt_pth)

    return regenerate_dir(src_pth, tgt_pth, cfg, overwrite_file)


def _rg_file(src_pth, tgt_name, tgt_pth, cfg, overwrite_file):
    """Regenerate a single file.

    Args:
        src_pth (str): path to file
        tgt_name (str): name of file to create
        tgt_pth (str): path to created file
        cfg (Config):  current package configuration
        overwrite_file (dict): which files to overwrite

    Returns:
        (dict|None): bid, hash of block content
    """
    if splitext(tgt_name)[0] == "_":
        return None

    LOGGER.debug("render file '%s' into '%s'", src_pth, tgt_pth)

    if overwrite_file.get(pth_as_key(tgt_pth), True):
        _, ext = splitext(tgt_name)
        if ext in NON_BIN_EXT:
            blocks = render(cfg, src_pth, tgt_pth)
            return dict((bid, compute_hash(cnt)) for bid, cnt in blocks)
        else:  # binary file
            if exists(tgt_pth):
                print("overwrite? %s" % tgt_pth)
            else:
                with open(src_pth, 'rb') as fhr:
                    content = fhr.read()
                with open(tgt_pth, 'wb') as fhw:
                    fhw.write(content)


def regenerate_dir(src_dir, tgt_dir, cfg, overwrite_file):
    """Walk all files in src_dir and create/update them on tgt_dir

    Args:
        src_dir (str): path to reference files
        tgt_dir (str): path to target where files will be written
        cfg (Config):  current package configuration
        overwrite_file (dict of str, bool): whether or not to overwrite some
                             files

    Returns:
        (dict of str, map): hash key of preserved sections
    """
    hmap = {}

    for src_name in listdir(src_dir):
        src_pth = src_dir + "/" + src_name
        tgt_name = cfg.render(src_name)
        if tgt_name.endswith(".tpl"):
            tgt_name = tgt_name[:-4]

        tgt_pth = tgt_dir + "/" + tgt_name
        # handle namespace
        if isdir(src_pth) and basename(src_dir) == 'src' and src_name == TPL_SRC_NAME:
            namespace = cfg['base']['namespace']
            if namespace is not None:
                ns_pth = tgt_dir + "/" + namespace
                if not exists(ns_pth):
                    mkdir(ns_pth)

                init_namespace_dir(ns_pth, cfg)
                tgt_pth = ns_pth + "/" + tgt_name

        if isdir(src_pth):
            hmap.update(_rg_dir(src_pth, tgt_name, tgt_pth, cfg, overwrite_file))
        else:
            bhash = _rg_file(src_pth, tgt_name, tgt_pth, cfg, overwrite_file)
            if bhash is not None:
                hmap[pth_as_key(tgt_pth)] = bhash

    return hmap
