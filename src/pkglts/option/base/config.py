"""
Set of function related to handling the configuration of this option.
"""
from os.path import abspath, basename


def update_parameters(cfg):
    """Update config with parameters necessary for this option.

    Notes: create a section with option name to store params.

    Args:
        cfg (dict): dict of option parameters as seen in pkg_cfg.json

    Returns:
        None: update in place
    """
    sec = dict(
        pkgname=basename(abspath(".")),
        namespace=None,
        namespace_method="pkg_util",
        url=None,
        authors=[("moi", "moi@email.com")]
    )
    cfg['base'] = sec


def is_valid_identifier(name):
    """ Check that name is a valid python identifier
    sort of back port of "".isidentifier()
    """
    try:
        compile("%s=1" % name, "test", 'single')
        return True
    except SyntaxError:
        return False


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    pkgname = cfg['base']['pkgname']
    namespace = cfg['base']['namespace']

    if "." in pkgname:
        invalids.append('base.pkgname')
    elif not is_valid_identifier(pkgname):
        invalids.append('base.pkgname')

    if namespace is not None:
        if "." in namespace:
            invalids.append('base.namespace')
        elif not is_valid_identifier(namespace):
            invalids.append('base.namespace')

    if cfg['base']['namespace_method'] not in ("pkg_util", "setuptools", "P3.3>"):
        invalids.append("base.namespace_method")

    return invalids


def require(purpose, cfg):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        cfg (Config):  current package configuration

    Returns:
        (list of Dependency)
    """
    del cfg, purpose

    return []
