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
        intended_versions=["36"],
        require=[]
    )
    cfg['pysetup'] = sec


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    intended_versions = cfg['pysetup']['intended_versions']

    if len(intended_versions) == 0:
        invalids.append("pysetup.intended_versions")

    require = cfg['pysetup']['require']

    valid_methods = (None, "pip", "conda", "git")
    if any(dep.get('pkg_mng') not in valid_methods for dep in require):
        invalids.append("pysetup.require")

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
        options = ['base', 'test', 'doc', 'license', 'version']
        return [Dependency(name) for name in options]

    return []
