from os.path import dirname

from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionLandscape(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def require_option(self):
        return ['doc', 'gtihub', 'flake8', 'travis']

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project']

        url = "landscape.io/github/%s/%s/master" % (owner, project)
        img = url + "/landscape.svg?style=flat"
        badge = fmt_badge(img, url, "Code health status", cfg['doc']['fmt'])

        return {"badge": badge}
