from os.path import dirname

from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionAppveyor(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            token=""
        )
        cfg[self._name] = sec

    def require_option(self):
        return ['doc', 'pysetup', 'github']

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project'].replace("_", "-")
        token = cfg[self._name]['token']

        url = "ci.appveyor.com/project/%s/%s/branch/master" % (owner, project)
        img = "ci.appveyor.com/api/projects/status/%s/branch/master?svg=true" % token
        badge = fmt_badge(img, url, "Appveyor build status", cfg['doc']['fmt'])

        return {"badge": badge}
