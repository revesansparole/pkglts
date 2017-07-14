from pkglts.dependency import Dependency

parameters = [
    ("major", 0),
    ("minor", 1),
    ("post", 0)
]


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
        invalids.append("major")
    if not isinstance(minor, int):
        invalids.append("minor")
    if not isinstance(post, int):
        invalids.append("post")

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
