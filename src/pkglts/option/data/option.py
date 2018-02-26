from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option


class OptionData(Option):
    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            filetype=[".json", ".ini"],
            use_ext_dir=False
        )
        cfg['data'] = sec

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['base']
            return [Dependency(name) for name in options]

        return []
