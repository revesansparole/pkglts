from pkglts.dependency import Dependency

parameters = [
    ("owner", "{{ base.authors[0][0] }}"),
    ("project", "{{ base.pkgname }}"),
    ("url", "https://github.com/{{ github.owner }}/{{ github.project }}")
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    project = env.globals['github'].project

    if len(project) == 0:
        invalids.append('project')

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
