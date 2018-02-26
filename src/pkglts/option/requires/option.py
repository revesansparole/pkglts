from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option


class OptionRequires(Option):
    def root_dir(self):
        return dirname(__file__)

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['doc', 'github']
            return [Dependency(name) for name in options]

        return []

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project']

        base_url = "requires.io/github/%s/%s/" % (owner, project)
        url = base_url + "requirements/?branch=master"
        img = base_url + "requirements.svg?branch=master"
        badge = fmt_badge(img, url, "Requirements status", cfg['doc']['fmt'])

        return {"badge": badge}
