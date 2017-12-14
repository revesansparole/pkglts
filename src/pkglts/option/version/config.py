"""
Set of function related to handling the configuration of this option.
"""
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
        major=0,
        minor=0,
        post=1,
    )
    cfg['version'] = sec


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    major = cfg['version']['major']
    minor = cfg['version']['minor']
    post = cfg['version']['post']

    if not isinstance(major, int):
        invalids.append("version.major")
    if not isinstance(minor, int):
        invalids.append("version.minor")
    if not isinstance(post, int):
        invalids.append("version.post")

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
        options = ['base']
        return [Dependency(name) for name in options]

    return []
