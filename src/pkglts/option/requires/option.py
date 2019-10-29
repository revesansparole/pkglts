from pathlib import Path

from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionRequires(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self):
        return ['doc', 'github']

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project']

        base_url = f"requires.io/github/{owner}/{project}/"
        url = f"{base_url}requirements/?branch=master"
        img = f"{base_url}requirements.svg?branch=master"
        badge = fmt_badge(img, url, "Requirements status", cfg['doc']['fmt'])

        return {"badge": badge}
