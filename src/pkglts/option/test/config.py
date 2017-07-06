from pkglts.dependency import Dependency

parameters = [
    ("suite_name", "pytest")
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    name = env.globals['test'].suite_name

    if name not in ("pytest", "nose"):
        invalids.append('suite_name')

    return invalids


def require(purpose, env):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        env (jinja2.Environment):  current working environment

    Returns:
        (list of Dependency)
    """
    if purpose == 'option':
        options = ['base']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        deps = [Dependency('mock')]

        test_suite = env.globals['test'].suite_name
        if test_suite == 'pytest':
            deps.append(Dependency('pytest'))
        if test_suite == 'nose':
            deps.append(Dependency('nose'))

        return deps

    return []
