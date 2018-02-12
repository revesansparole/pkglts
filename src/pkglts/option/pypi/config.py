"""
Set of function related to handling the configuration of this option.
"""
from pkglts.dependency import Dependency


def update_parameters(cfg):
    """Update config with parameters necessary for this option.

    Notes: create a section with option name to store params.

    Args:
        cfg (dict): dict of option parameters as seen in pkg_cfg.json

    Returns:
        None: update in place
    """
    sec = dict(
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Natural Language :: English"
        ],
        servers=[
            dict(name="pypi", url="https://upload.pypi.org/legacy/"),
            dict(name="test", url="https://testpypi.python.org/pypi")
        ]
    )
    cfg['pypi'] = sec


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    classifiers = cfg['pypi']['classifiers']

    if not classifiers:
        invalids.append("pypi.classifiers")

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
        options = ['pysetup']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        return [Dependency('twine', pkg_mng='pip')]

    return []
