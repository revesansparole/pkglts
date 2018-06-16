from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionFlake8(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['base']
            return [Dependency(name) for name in options]

        if purpose == 'dvlpt':
            return [Dependency('flake8')]

        return []
