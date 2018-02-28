from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option


def is_valid_identifier(name):
    """ Check that name is a valid python identifier
    sort of back port of "".isidentifier()
    """
    try:
        compile("%s=1" % name, "test", 'single')
        return True
    except SyntaxError:
        return False


class OptionPluginProject(Option):
    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        cfg['plugin_project'] = {
            "plugin_name": "{{ base.pkgname }}"
        }

    def check(self, cfg):
        invalids = []
        plugin_name = cfg['plugin_project']['plugin_name']

        if "." in plugin_name:
            invalids.append('plugin_project.plugin_name')
        elif not is_valid_identifier(plugin_name):
            invalids.append('plugin_project.plugin_name')

        return invalids

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['pysetup', 'data', 'github']
            return [Dependency(name) for name in options]

        if purpose == 'install':
            return [Dependency('pkglts')]

        return []
