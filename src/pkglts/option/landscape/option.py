from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option


class OptionLandscape(Option):
    def root_dir(self):
        return dirname(__file__)

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['doc', 'github', 'flake8', 'travis']
            return [Dependency(name) for name in options]

        return []

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project']

        url = "landscape.io/github/%s/%s/master" % (owner, project)
        img = url + "/landscape.svg?style=flat"
        badge = fmt_badge(img, url, "Code health status", cfg['doc']['fmt'])

        return {"badge": badge}
