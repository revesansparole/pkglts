"""
Set of function to extend jinja2 environment.
"""
from pkglts.local import pkg_full_name, src_dir


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    return {"pkg_full_name": pkg_full_name(cfg),
            "src_pth": src_dir(cfg)}
