from pkglts.dependency import Dependency


def update_parameters(cfg):
    """Update config with parameters necessary for this option.

    Notes: create a section with option name to store params.

    Args:
        cfg (dict): dict of option parameters as seen in pkg_cfg.json

    Returns:
        None: update in place
    """
    cfg['plugin_project'] = {
        "plugin_name": "{{ base.pkgname }}"
    }
    # empty project just for construction
    # so does nothing
    # del cfg
    # return


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
    plugin_name = cfg['plugin_project']['plugin_name']

    if "." in plugin_name:
        invalids.append('plugin.plugin_name')
    elif not is_valid_identifier(plugin_name):
        invalids.append('plugin.plugin_name')

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
        options = ['pysetup', 'data', 'github']
        return [Dependency(name) for name in options]

    if purpose == 'install':
        return [Dependency('pkglts')]

    return []
