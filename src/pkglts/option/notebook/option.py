import logging
from pathlib import Path

from pkglts.option_object import Option
from pkglts.version import __version__
from . import nbcompile

LOGGER = logging.getLogger(__name__)


class OptionNotebook(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        LOGGER.info("update parameters %s", self._name)
        sec = dict(src_directory="example")
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        src_directory = Path(cfg[self._name]["src_directory"])

        if not src_directory.exists():
            invalids.append("notebook.src_directory")

        return invalids

    def require_option(self, cfg):
        return ["sphinx"]

    def tools(self, cfg):
        del cfg
        yield nbcompile.parser_nbcompile
