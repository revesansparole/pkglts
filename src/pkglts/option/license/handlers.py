import logging
from os.path import dirname
from os.path import join as pj

from pkglts.templating import replace


logger = logging.getLogger(__name__)

tpl_dir = pj(dirname(__file__), "templates")


def get_tpl_path(name):
    """Return a path for license template file.

    .. warning:: Do not test if path exists

    args:
     - name (str): name of license to fetch

    return:
     - (str)
    """
    tpl_pth = pj(tpl_dir, "%s.txt" % name.lower())
    return tpl_pth


def generate(txt, env):
    """ Ignore txt and generate a license
    """
    del txt  # unused
    name = env['license']['name']

    # open template
    try:
        with open(get_tpl_path(name), 'r') as f:
            cnt = f.read()

        txt = replace(cnt, {}, env)
        return "\n" + txt
    except IOError as e:
        logger.error("unable to find template for given license")
        raise e


def setup_handler(txt, env):
    del txt  # unused
    return '\n    license="%s",' % env['license']['name']


mapping = {"license.generate": generate,
           "license.setup": setup_handler}
