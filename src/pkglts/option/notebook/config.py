from os.path import exists

from pkglts.dependency import Dependency

parameters = [
    ("src_directory", "example")
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    src_directory = env.globals['notebook'].src_directory

    if not exists(src_directory):
        invalids.append("src_directory")

    return invalids


def require(purpose, env):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        env (jinja2.Environment):  current working environment

    Returns:
        (list of Dependency)
    """
    del env

    if purpose == 'option':
        options = ['sphinx']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        return [Dependency('nbconvert')]

    return []
