from os.path import dirname

from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionRequires(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def require_option(self):
        return ['doc', 'github']

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project']

        base_url = "requires.io/github/%s/%s/" % (owner, project)
        url = base_url + "requirements/?branch=master"
        img = base_url + "requirements.svg?branch=master"
        badge = fmt_badge(img, url, "Requirements status", cfg['doc']['fmt'])

        return {"badge": badge}
