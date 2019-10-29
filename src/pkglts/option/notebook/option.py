from pathlib import Path

from pkglts.option_object import Option
from pkglts.version import __version__

from . import nbcompile


class OptionNotebook(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        sec = dict(
            src_directory="example"
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        src_directory = Path(cfg[self._name]['src_directory'])

        if not src_directory.exists():
            invalids.append("notebook.src_directory")

        return invalids

    def require_option(self):
        return ['sphinx']

    def tools(self, cfg):
        del cfg
        yield nbcompile.parser_nbcompile
