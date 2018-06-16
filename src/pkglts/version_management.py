"""
Set of function to store the version of each option each time the package is
regenerated and access them later to prevent reverting changes.
"""
import json
import logging
from os.path import join as pj

from .config import pkg_version_file, pkglts_dir
from .option_tools import available_options

LOGGER = logging.getLogger(__name__)


def load_pkg_version(rep="."):
    """Read version file associated to this package.

    Args:
        rep (str): directory to search for info

    Returns:
        (dict of str, str): option name, version
    """
    with open(pj(rep, pkglts_dir, pkg_version_file), 'r') as fhr:
        return json.load(fhr)


def write_pkg_version(cfg, rep="."):
    """Store version of tools associated to this package on disk.

    Args:
        cfg (Config): current working config
        rep (str): directory to search for info

    Returns:
        None
    """
    LOGGER.info("write package version")

    ver = {opt_name: available_options[opt_name].version() for opt_name in cfg.installed_options()}

    with open(pj(rep, pkglts_dir, pkg_version_file), 'w') as fhw:
        json.dump(ver, fhw, sort_keys=True, indent=2)
