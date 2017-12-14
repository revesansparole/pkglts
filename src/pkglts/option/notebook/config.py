"""
Set of function related to handling the configuration of this option.
"""
from os.path import exists

from pkglts.dependency import Dependency


def update_parameters(cfg):
    """Update config with parameters necessary for this option.

    Notes: create a section with option name to store params.

    Args:
        cfg (dict): dict of option parameters as seen in pkg_cfg.json

    Returns:
        None: update in place
    """
    sec = dict(
        src_directory="example"
    )
    cfg['notebook'] = sec


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    src_directory = cfg['notebook']['src_directory']

    if not exists(src_directory):
        invalids.append("notebook.src_directory")

    return invalids


def require(purpose, cfg):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        cfg (Config):  current package configuration

    Returns:
        (list of Dependency)
    """
    del cfg

    if purpose == 'option':
        options = ['sphinx']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        return [Dependency('nbconvert')]

    return []
