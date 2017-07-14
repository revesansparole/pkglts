from pkglts.dependency import Dependency

parameters = [
    ("description", "belle petite description"),
    ("keywords", [])
]


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    description = cfg['doc']['description']
    # keywords = env.globals['doc'].keywords

    if len(description) == 0:
        invalids.append("description")

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
