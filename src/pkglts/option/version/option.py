import logging
from pathlib import Path

from pkglts.option_object import Option
from pkglts.version import __version__
from . import bump_version

LOGGER = logging.getLogger(__name__)


class OptionVersion(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        LOGGER.info("update parameters %s", self._name)
        sec = dict(
            major=0,
            minor=0,
            post=1,
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        major = cfg[self._name]['major']
        minor = cfg[self._name]['minor']
        post = cfg[self._name]['post']

        if not isinstance(major, int):
            invalids.append("version.major")
        if not isinstance(minor, int):
            invalids.append("version.minor")
        if not isinstance(post, int):
            invalids.append("version.post")

        return invalids

    def require_option(self, cfg):
        return ['src']

    def tools(self, cfg):
        del cfg
        yield bump_version.parser_bump
