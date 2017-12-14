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
        owner="{{ base.authors[0][0] }}",
        project="{{ base.pkgname }}",
        server="framagit.org",
        url="https://{{ gitlab.server }}/{{ gitlab.owner }}/{{ gitlab.project }}"
    )
    cfg['gitlab'] = sec


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    project = cfg['gitlab']['project']

    if not project:
        invalids.append('gitlab.project')

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
        options = ['git']
        return [Dependency(name) for name in options]

    return []
