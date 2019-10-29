"""
Set of function to store the version of each option each time the package is
regenerated and access them later to prevent reverting changes.
"""
import json
import logging

import semver

from .config import pkg_version_file, pkglts_dir
from .option_tools import available_options

LOGGER = logging.getLogger(__name__)


def load_pkg_version(rep="."):
    """Read version file associated to this package.

    Args:
        rep (Path): directory to search for info

    Returns:
        (dict of str, str): option name, version
    """
    with open(rep / pkglts_dir / pkg_version_file, 'r') as fhr:
        return json.load(fhr)


def write_pkg_version(cfg, rep="."):
    """Store version of tools associated to this package on disk.

    Args:
        cfg (Config): current working config
        rep (Path): directory to search for info

    Returns:
        None
    """
    LOGGER.info("write package version")

    ver = {name: option_current_version(name) for name in cfg.installed_options()}

    with open(rep / pkglts_dir / pkg_version_file, 'w') as fhw:
        json.dump(ver, fhw, sort_keys=True, indent=2)


def option_current_version(name):
    """Get current version of a given option.

    Args:
        name (str): name of option

    Returns:
        (str): X.X.X
    """
    return available_options[name].version()


def outdated_options(cfg, rep="."):
    """Find options which actual version is too old.

    An option is outdated if it's current version is older
    than the version used to regenerate the package.

    Args:
        cfg (Config): current working config
        rep (Path): directory to search for info

    Returns:
        (list of str): list of option names
    """
    try:
        ver = load_pkg_version(rep)
    except FileNotFoundError:
        return []

    outdated = []
    for name in cfg.installed_options():
        ver_cur = option_current_version(name)
        ver_last_rg = ver.get(name, "0.0.0")
        if semver.compare(ver_cur, ver_last_rg) < 0:
            outdated.append(name)

    return outdated
