from os.path import dirname

from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionTravis(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def require_option(self):
        return ['doc', 'pysetup', 'github']

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project']

        url = "travis-ci.org/%s/%s" % (owner, project)
        img = url + ".svg?branch=master"
        badge = fmt_badge(img, url, "Travis build status", cfg['doc']['fmt'])

        return {"badge": badge}
