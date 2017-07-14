from os.path import exists

from pkglts.dependency import Dependency

from .handlers import get_tpl_path


def update_parameters(cfg):
    """Update config with parameters necessary for this option.

    Notes: create a section with option name to store params.

    Args:
        cfg (dict): dict of option parameters as seen in pkg_cfg.json

    Returns:
        None: update in place
    """
    sec = dict(
        name="cecill-c",
        year=2017,
        organization="organization",
        project="{{ base.pkgname }}"
    )
    cfg['license'] = sec


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    name = cfg['license']['name']
    # year = pkg_cfg['license']['year']
    # organization = pkg_cfg['license']['organization']
    # project = pkg_cfg['license']['project']

    if len(name) == 0:
        invalids.append('name')
    elif not exists(get_tpl_path(name)):
        invalids.append('name')

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
