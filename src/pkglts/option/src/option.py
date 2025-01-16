import logging
from pathlib import Path

from pkglts.local import src_dir
from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionSrc(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        LOGGER.info("update parameters %s", self._name)
        sec = dict(
            namespace_method="pkg_util",
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []

        if cfg[self._name]["namespace_method"] not in ("pkg_util", "setuptools", "P3.3>"):
            invalids.append("src.namespace_method")

        return invalids

    def require_option(self, cfg):
        return ["base"]

    def environment_extensions(self, cfg):
        return {"src_pth": src_dir(cfg).as_posix()}
