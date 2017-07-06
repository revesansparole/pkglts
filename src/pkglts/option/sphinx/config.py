from pkglts.dependency import Dependency

parameters = [
    ("theme", 'default'),
    ("autodoc_dvlpt", True)
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    theme = env.globals['sphinx'].theme
    if theme != str(theme):
        invalids.append('theme')

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
        options = ['test', 'doc']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        return [Dependency('sphinx')]

    return []
