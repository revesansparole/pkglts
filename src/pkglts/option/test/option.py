from pathlib import Path

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionTest(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        sec = dict(
            suite_name="pytest",
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        name = cfg[self._name]['suite_name']

        if name not in ("pytest", "nose"):
            invalids.append('test.suite_name')

        return invalids

    def require_option(self):
        return ['pysetup']

    def require(self, cfg):
        test_suite = cfg['test']['suite_name']
        if test_suite == 'pytest':
            yield Dependency('pytest', intent='test')
            yield Dependency('pytest-mock', intent='test')
        elif test_suite == 'nose':
            yield Dependency('nose', intent='test')
            yield Dependency('mock', intent='test')
