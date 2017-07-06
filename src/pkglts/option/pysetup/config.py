from pkglts.dependency import Dependency

parameters = [
    ("intended_versions", ["27"]),
    ("require", [])
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    intended_versions = env.globals['pysetup'].intended_versions

    if len(intended_versions) == 0:
        invalids.append("intended_versions")

    require = env.globals['pysetup'].require

    valid_methods = ("none", "pip", "conda", "git")
    if any(dep.get('pkg_mng', 'none') not in valid_methods for dep in require):
        invalids.append("require")

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
        options = ['base', 'test', 'doc', 'license', 'version']
        return [Dependency(name) for name in options]

    return []
