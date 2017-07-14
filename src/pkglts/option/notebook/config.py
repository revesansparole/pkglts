from os.path import exists

from pkglts.dependency import Dependency

parameters = [
    ("src_directory", "example")
]


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    src_directory = cfg['notebook']['src_directory']

    if not exists(src_directory):
        invalids.append("src_directory")

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
        options = ['sphinx']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        return [Dependency('nbconvert')]

    return []
