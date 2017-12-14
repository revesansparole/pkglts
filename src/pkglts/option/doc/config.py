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
        description="belle petite description",
        fmt="rst",
        keywords=[]
    )
    cfg['doc'] = sec


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    description = cfg['doc']['description']
    fmt = cfg['doc']['fmt']
    # keywords = env.globals['doc'].keywords

    if len(description) == 0:
        invalids.append("doc.description")

    if fmt not in ('rst', 'md'):
        invalids.append("doc.fmt")

    return invalids


def require(purpose, cfg):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        cfg (Config):  current package configuration

    Returns:
        (list of Dependency)
    """
    if purpose == 'option':
        options = ['base']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        if cfg['doc']['fmt'] == 'md':
            return [Dependency('mkdocs', pkg_mng='pip')]

    return []
