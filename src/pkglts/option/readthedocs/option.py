from os.path import dirname

from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionReadthedocs(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            project="{{ github.project }}"
        )
        cfg['readthedocs'] = sec

    def check(self, cfg):
        invalids = []
        project = cfg['readthedocs']['project']

        if not project:
            invalids.append("readthedocs.project")

        return invalids

    def require_option(self):
        return ['doc', 'pysetup', 'github', 'sphinx']

    def environment_extensions(self, cfg):
        project = cfg['readthedocs']['project']
        project = project.replace(".", "")
        url = "%s.readthedocs.io/en/latest/?badge=latest" % project
        img = "readthedocs.org/projects/%s/badge/?version=latest" % project
        badge = fmt_badge(img, url, "Documentation status", cfg['doc']['fmt'])

        return {"badge": badge}
