import logging
from pathlib import Path

from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionGithub(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        LOGGER.info("update parameters %s", self._name)
        sec = dict(
            owner="{{ base.authors[0][0] }}",
            project="{{ base.pkgname }}",
            url="https://github.com/{{ github.owner }}/{{ github.project }}",
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        project = cfg[self._name]["project"]

        if not project:
            invalids.append("github.project")

        return invalids

    def require_option(self, cfg):
        return ["git"]
