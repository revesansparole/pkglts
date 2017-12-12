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
        suite_name="pytest",
    )
    cfg['test'] = sec


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    name = cfg['test']['suite_name']

    if name not in ("pytest", "nose"):
        invalids.append('test.suite_name')

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
        test_suite = cfg['test']['suite_name']
        if test_suite == 'pytest':
            return [Dependency(name) for name in ['pytest', 'pytest-mock']]
        if test_suite == 'nose':
            return [Dependency(name) for name in ['nose', 'mock']]

    return []
