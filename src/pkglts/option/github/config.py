from pkglts.dependency import Dependency

parameters = [
    ("owner", "{{ base.authors[0][0] }}"),
    ("project", "{{ base.pkgname }}"),
    ("url", "https://github.com/{{ github.owner }}/{{ github.project }}")
]


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    project = cfg['github']['project']

    if len(project) == 0:
        invalids.append('project')

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
