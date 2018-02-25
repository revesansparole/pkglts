from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option


class OptionTravis(Option):
    def root_dir(self):
        return dirname(__file__)

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['doc', 'pysetup', 'github']
            return [Dependency(name) for name in options]

        return []

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project']

        url = "travis-ci.org/%s/%s" % (owner, project)
        img = url + ".svg?branch=master"
        badge = fmt_badge(img, url, "Travis build status", cfg['doc']['fmt'])

        return {"badge": badge}
