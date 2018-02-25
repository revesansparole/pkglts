from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option


class OptionConda(Option):
    def root_dir(self):
        return dirname(__file__)

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['pysetup']
            return [Dependency(name) for name in options]

        return []
