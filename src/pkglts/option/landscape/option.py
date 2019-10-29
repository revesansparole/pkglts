from pathlib import Path

from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionLandscape(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self):
        return ['flake8', 'travis']

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project']

        url = f"landscape.io/github/{owner}/{project}/master"
        img = f"{url}/landscape.svg?style=flat"
        badge = fmt_badge(img, url, "Code health status", cfg['doc']['fmt'])

        return {"badge": badge}
