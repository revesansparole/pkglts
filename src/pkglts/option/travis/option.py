from pathlib import Path

from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionTravis(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self):
        return ['doc', 'pysetup', 'github']

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project']

        url = f"api.travis-ci.com/{owner}/{project}"
        img = f"{url}.svg?branch=master"
        badge = fmt_badge(img, url, "Travis build status", cfg['doc']['fmt'])

        return {"badge": badge}
