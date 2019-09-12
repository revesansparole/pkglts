from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.small_tools import is_valid_identifier
from pkglts.version import __version__


class OptionPluginProject(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        cfg[self._name] = {
            "plugin_name": "{{ base.pkgname }}"
        }

    def check(self, cfg):
        invalids = []
        plugin_name = cfg[self._name]['plugin_name']

        if "." in plugin_name:
            invalids.append('plugin_project.plugin_name')
        elif not is_valid_identifier(plugin_name):
            invalids.append('plugin_project.plugin_name')

        return invalids

    def require_option(self):
        return ['pysetup', 'data', 'git']

    def require(self, cfg):
        del cfg
        yield Dependency('pkglts', intent='install', channel='revesansparole')
