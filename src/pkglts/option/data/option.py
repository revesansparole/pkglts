from pathlib import Path

from pkglts.option_object import Option
from pkglts.version import __version__


class OptionData(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        sec = dict(
            filetype=[".json", ".ini"],
            use_ext_dir=False
        )
        cfg[self._name] = sec

    def require_option(self, cfg):
        return ['src']
