from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from {{ base.pkg_full_name }}.version import __version__


class Option{{ plugin_project.plugin_name|capitalize }}(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        # you can modify other sections here
        # but be careful not to mess up with other options

        # add a parameter to the option
        cfg['{{ plugin_project.plugin_name }}'] = dict(myparam='custom_param')

    def check(self, cfg):
        invalids = []
        myparam = cfg['{{ plugin_project.plugin_name }}']['myparam']

        if myparam != 'custom_param':
            invalids.append("myparam")

        return invalids

    def require_option(self):
        return ['base']

    def require(self, cfg):
        del cfg
        yield Dependency('pkglts', intent='install')
