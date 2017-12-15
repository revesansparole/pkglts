"""
Set of function to extend jinja2 environment.
"""
import logging
from os.path import dirname
from os.path import join as pj

LOGGER = logging.getLogger(__name__)

TPL_DIR = pj(dirname(__file__), "templates")


def get_tpl_path(name):
    """Return a path for license template file.

    Warnings: Do not test if path exists

    Args:
        name (str): name of license to fetch

    Returns:
        (str)
    """
    return pj(TPL_DIR, "%s.txt" % name.lower())


def full_text(cfg):
    """Generate a license
    """
    name = cfg['license']['name']

    # open template
    try:
        with open(get_tpl_path(name), 'r') as fhr:
            cnt = fhr.read()

        return cfg.render(cnt)
    except IOError as err:
        LOGGER.error("unable to find template for given license")
        raise err


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    return {"full_text": full_text(cfg)}
