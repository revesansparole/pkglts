from pkglts.dependency import Dependency

parameters = [
    ("major", 0),
    ("minor", 1),
    ("post", 0)
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    major = env.globals['version'].major
    minor = env.globals['version'].minor
    post = env.globals['version'].post

    if not isinstance(major, int):
        invalids.append("major")
    if not isinstance(minor, int):
        invalids.append("minor")
    if not isinstance(post, int):
        invalids.append("post")

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
        options = ['base']
        return [Dependency(name) for name in options]

    return []
