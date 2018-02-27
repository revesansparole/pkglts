from os.path import dirname, exists

from pkglts.dependency import Dependency
from pkglts.option_object import Option

from . import nbcompile


class OptionNotebook(Option):
    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            src_directory="example"
        )
        cfg['notebook'] = sec

    def check(self, cfg):
        invalids = []
        src_directory = cfg['notebook']['src_directory']

        if not exists(src_directory):
            invalids.append("notebook.src_directory")

        return invalids

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['sphinx']
            return [Dependency(name) for name in options]

        if purpose == 'dvlpt':
            return [Dependency('nbconvert')]

        return []

    def tools(self, cfg):
        del cfg
        yield nbcompile.parser_nbcompile
