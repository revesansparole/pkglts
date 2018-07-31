from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionTox(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def require_option(self):
        return ['pysetup']

    def require(self, cfg):
        del cfg
        yield Dependency('tox', intent='test')
