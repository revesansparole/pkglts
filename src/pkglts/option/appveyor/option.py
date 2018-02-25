from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option


class OptionAppveyor(Option):
    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            token=""
        )
        cfg['appveyor'] = sec

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['doc', 'pysetup', 'github']
            return [Dependency(name) for name in options]

        return []

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project'].replace("_", "-")
        token = cfg['appveyor']['token']

        url = "ci.appveyor.com/project/%s/%s/branch/master" % (owner, project)
        img = "ci.appveyor.com/api/projects/status/%s/branch/master?svg=true" % token
        badge = fmt_badge(img, url, "Appveyor build status", cfg['doc']['fmt'])

        return {"badge": badge}
