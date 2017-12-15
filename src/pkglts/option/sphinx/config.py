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
        theme="default",
        autodoc_dvlpt=True,
        build_dir="build/sphinx"
    )
    cfg['sphinx'] = sec


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    if cfg['doc']['fmt'] != 'rst':
        invalids.append('doc.fmt')

    theme = cfg['sphinx']['theme']
    if theme != str(theme):
        invalids.append('sphinx.theme')

    return invalids


def require(purpose, cfg):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        cfg (Config):  current package configuration

    Returns:
        (list of Dependency)
    """
    if purpose == 'option':
        options = ['test', 'doc', 'license']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        deps = [Dependency('sphinx')]
        if cfg["sphinx"]["theme"] == "sphinx_rtd_theme":
            deps.append(Dependency('sphinx_rtd_theme'))

        return deps

    return []
