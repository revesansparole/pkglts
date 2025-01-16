import logging
from pathlib import Path

from pkglts.option_object import Option
from pkglts.version import __version__
from pkglts.dependency import normalize
from pkglts.local import pkg_full_name

LOGGER = logging.getLogger(__name__)


class OptionCondaAlias(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self, cfg):
        return ["conda"]

    def environment_extensions(self, cfg):
        return {"norm_name": normalize(pkg_full_name(cfg))}
