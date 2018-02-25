import logging
from datetime import datetime
from os.path import dirname, exists
from os.path import join as pj

from pkglts.dependency import Dependency
from pkglts.option_object import Option

LOGGER = logging.getLogger(__name__)

TPL_DIR = pj(dirname(__file__), "templates")


class OptionLicense(Option):
    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            name="cecill-c",
            year=datetime.now().year,
            organization="organization",
            project="{{ base.pkgname }}"
        )
        cfg['license'] = sec

    def check(self, cfg):
        invalids = []
        name = cfg['license']['name']
        # year = pkg_cfg['license']['year']
        # organization = pkg_cfg['license']['organization']
        # project = pkg_cfg['license']['project']

        if not name or not exists(get_tpl_path(name)):
            invalids.append('license.name')

        return invalids

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['base']
            return [Dependency(name) for name in options]

        return []

    def environment_extensions(self, cfg):
        return {"full_text": full_text(cfg)}


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
