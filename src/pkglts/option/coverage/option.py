from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option


class OptionCoverage(Option):
    def root_dir(self):
        return dirname(__file__)

    def require(self, purpose, cfg):
        if purpose == 'option':
            options = ['test']
            return [Dependency(name) for name in options]

        if purpose == 'dvlpt':
            deps = [Dependency('coverage')]
            test_suite = cfg['test']['suite_name']
            if test_suite == 'pytest':
                deps.append(Dependency('pytest-cov'))

            return deps

        return []
