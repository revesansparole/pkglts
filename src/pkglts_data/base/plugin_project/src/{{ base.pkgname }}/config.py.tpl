from pkglts.dependency import Dependency


def update_parameters(cfg):
    """Update config with parameters necessary for this option.

    Notes: create a section with option name to store params.

    Args:
        cfg (dict): dict of option parameters as seen in pkg_cfg.json

    Returns:
        None: update in place
    """
    # you can modify other sections here
    # but be careful not to mess up with other options

    # add a parameter to the option
    cfg['{{ base.pkgname }}'] = dict(myparam='custom_param')


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    myparam = cfg['{{ base.pkgname }}']['myparam']

    if myparam != 'custom_param':
        invalids.append("myparam")

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
        options = ['pysetup', 'data']
        return [Dependency(name) for name in options]

    if purpose == 'install':
        return [Dependency('pkglts')]

    return []
