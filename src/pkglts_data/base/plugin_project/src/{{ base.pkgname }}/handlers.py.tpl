"""Used to extend Jinja2 environment with extra arguments
"""


def installed_options(cfg):
    return ",".join(cfg.keys())


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    return {"pkg_installed_options": installed_options(cfg)}
