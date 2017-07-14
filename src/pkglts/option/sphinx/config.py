from pkglts.dependency import Dependency

parameters = [
    ("theme", 'default'),
    ("autodoc_dvlpt", True)
]


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    theme = cfg['sphinx']['theme']
    if theme != str(theme):
        invalids.append('theme')

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
        options = ['test', 'doc']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        return [Dependency('sphinx')]

    return []
