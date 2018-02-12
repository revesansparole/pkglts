"""
Set of function to extend jinja2 environment.
"""
from pkglts.option_tools import available_options


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    badges = []
    for name in cfg.installed_options():
        if name != 'doc':
            opt = available_options[name]
            ext = opt.environment_extensions(cfg)
            if 'badge' in ext:
                badges.append(ext['badge'])
            if 'badges' in ext:
                badges.extend(ext['badges'])

    return {"badges": badges}
