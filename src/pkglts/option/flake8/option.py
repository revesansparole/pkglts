from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionFlake8(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def require_option(self):
        return ['base']

    def require(self, cfg):
        del cfg
        yield Dependency('flake8', intent='dvlpt')
