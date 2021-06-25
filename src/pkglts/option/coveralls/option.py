from pathlib import Path

from pkglts.dependency import Dependency
from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionCoveralls(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self, cfg):
        return ['coverage', 'travis']

    def require(self, cfg):
        del cfg
        yield Dependency('coveralls', intent='test')

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project']

        url = f"coveralls.io/github/{owner}/{project}?branch=master"
        img = f"coveralls.io/repos/github/{owner}/{project}/badge.svg?branch=master"
        badge = fmt_badge(img, url, "Coverage report status", cfg['doc']['fmt'])

        return {"badge": badge}
