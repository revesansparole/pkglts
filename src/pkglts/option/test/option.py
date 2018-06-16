from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionTest(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            suite_name="pytest",
        )
        cfg['test'] = sec

    def check(self, cfg):
        invalids = []
        name = cfg['test']['suite_name']

        if name not in ("pytest", "nose"):
            invalids.append('test.suite_name')

        return invalids

    def require(self, purpose, cfg):
        if purpose == 'option':
            options = ['base']
            return [Dependency(name) for name in options]

        if purpose == 'dvlpt':
            test_suite = cfg['test']['suite_name']
            if test_suite == 'pytest':
                return [Dependency(name) for name in ['pytest', 'pytest-mock']]
            if test_suite == 'nose':
                return [Dependency(name) for name in ['nose', 'mock']]

        return []
