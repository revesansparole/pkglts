from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.option.pysetup.option import requirements


class OptionConda(Option):
    def root_dir(self):
        return dirname(__file__)

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['pysetup']
            return [Dependency(name) for name in options]

        return []

    def environment_extensions(self, cfg):
        channels = set(dep.channel for dep in requirements(cfg, 'install'))
        try:
            channels.remove(None)
        except KeyError:
            pass

        return {"channels": channels}
