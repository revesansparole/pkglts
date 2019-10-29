from pathlib import Path

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionTox(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self):
        return ['pysetup']

    def require(self, cfg):
        del cfg
        yield Dependency('tox', intent='test', channel='conda-forge')
