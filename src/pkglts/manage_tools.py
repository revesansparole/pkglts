""" Specific helper function for manage script
"""

import logging

from .hash_management import compute_hash, pth_as_key
from .local import init_namespace_dir
from .option_tools import available_options, get_user_permission
from .templating import Template

LOGGER = logging.getLogger(__name__)

TPL_SRC_NAME = "{" + "{ base.pkgname }" + "}"


def check_option_parameters(name, cfg):
    """Check that the parameters associated to an option are valid.

    Args:
        name (str): option name
        cfg (Config):  current package configuration
    """
    opt = available_options[name]
    return opt.check(cfg)


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
        raise KeyError(f"option '{name}' does not exists")

    # find other option requirements in repository
    for option_name in opt.require_option():
        if option_name not in cfg.installed_options():
            LOGGER.info("need to install option '%s' first", option_name)
            if (cfg["_pkglts"]['auto_install'] or
                    get_user_permission("install")):
                cfg = update_opt(option_name, cfg)
            else:
                return cfg

    # find parameters required by option config
    opt.update_parameters(cfg.template())
    cfg.resolve()

    return cfg


def find_templates(src_dir, tgt_dir, cfg, rg_tree):
    """Find all template files associated to an option

    Warnings: modify rg_tree in place

    Args:
        src_dir (Path): path to reference files
        tgt_dir (Path): path to target where files will be written
        cfg (Config):  current package configuration
        rg_tree (dict): Structure to store path to templates found

    Returns:
        None
    """
    LOGGER.debug("find_templates in %s", src_dir)

    for src_pth in src_dir.glob("*"):
        tgt_name = cfg.render(src_pth.name)
        if tgt_name.endswith(".tpl"):
            tgt_name = tgt_name[:-4]

        tgt_pth = tgt_dir / tgt_name
        # handle namespace
        if src_pth.is_dir() and src_dir.name == 'src' and src_pth.name == TPL_SRC_NAME:
            namespace = cfg['base']['namespace']
            if namespace is not None:
                ns_pth = tgt_dir / namespace
                init_namespace_dir(ns_pth, rg_tree)
                tgt_pth = ns_pth / tgt_name

        if src_pth.is_dir():
            if tgt_name in ("", "_"):
                # do nothing
                pass
            else:
                find_templates(src_pth, tgt_pth, cfg, rg_tree)
        else:
            if tgt_name.split('.')[0] == "_":
                pass
            else:
                try:
                    rg_tree[pth_as_key(tgt_pth)].append(src_pth)
                except KeyError:
                    rg_tree[pth_as_key(tgt_pth)] = [src_pth]


def render_template(src_pths, tgt_pth, cfg, overwrite_file):
    """Render template and write it in tgt_pth

    Args:
        src_pths (list): list of reference templates
        tgt_pth (Path): path to created file
        cfg (Config):  current package configuration
        overwrite_file (dict): which files to overwrite

    Returns:
        (dict|None): bid, hash of block content
    """
    LOGGER.debug("render file '%s'", tgt_pth)
    if not overwrite_file.get(pth_as_key(tgt_pth), True):
        LOGGER.debug("no overwrite")
        return None

    tpl = Template()
    for src_pth in src_pths:
        tpl.parse(src_pth)

    blocks = tpl.render(cfg, tgt_pth)
    if blocks is None:
        return None
    else:  # non binary file
        return dict((bid, compute_hash(cnt)) for bid, cnt in blocks)
