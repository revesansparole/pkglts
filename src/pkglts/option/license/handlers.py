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


def full_text(env):
    """Generate a license
    """
    name = env.globals['license'].name

    # open template
    try:
        with open(get_tpl_path(name), 'r') as f:
            cnt = f.read()

        return env.from_string(cnt).render()
    except IOError as e:
        logger.error("unable to find template for given license")
        raise e


def environment_extensions(env):
    """Add more functionality to an environment.

    Args:
        env (jinja2.Environment):

    Returns:
        dict of str: any
    """
    return {"full_text": full_text(env)}
