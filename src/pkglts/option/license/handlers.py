import logging
from os.path import dirname
from os.path import join as pj


logger = logging.getLogger(__name__)

tpl_dir = pj(dirname(__file__), "templates")


def get_tpl_path(name):
    """Return a path for license template file.

    Warnings: Do not test if path exists

    Args:
        name (str): name of license to fetch

    Returns:
        (str)
    """
    tpl_pth = pj(tpl_dir, "%s.txt" % name.lower())
    return tpl_pth


def full_text(cfg):
    """Generate a license
    """
    name = cfg['license']['name']

    # open template
    try:
        with open(get_tpl_path(name), 'r') as f:
            cnt = f.read()

        return cfg.render(cnt)
    except IOError as e:
        logger.error("unable to find template for given license")
        raise e


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    return {"full_text": full_text(cfg)}
