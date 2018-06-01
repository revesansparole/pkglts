from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.option.pysetup.option import requirements


class OptionCoverage(Option):
    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            exclude_lines=[
                "raise AssertionError",
                "raise NotImplemented",
                "raise NotImplementedError"
            ],
        )
        cfg['coverage'] = sec

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

    def environment_extensions(self, cfg):
        if 'exclude_lines' in cfg['coverage'].keys():
            exclude_lines = cfg['coverage']['exclude_lines']
        else:
            exclude_lines = []
        return {"exclude_lines": exclude_lines}
