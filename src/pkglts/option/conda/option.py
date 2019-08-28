from os.path import dirname
from pkglts.option.reqs.option import requirements
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionConda(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def require_option(self):
        return ['pysetup']

    def environment_extensions(self, cfg):
        channels = set(dep.channel for dep in requirements(cfg)) - {None}

        return {"channels": channels}
