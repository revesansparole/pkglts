from pathlib import Path

from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionReadthedocs(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        sec = dict(
            project="{{ github.project }}"
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        project = cfg[self._name]['project']

        if not project:
            invalids.append("readthedocs.project")

        return invalids

    def require_option(self):
        return ['pysetup', 'github', 'sphinx']

    def environment_extensions(self, cfg):
        project = cfg['readthedocs']['project']
        project = project.replace(".", "")
        url = f"{project}.readthedocs.io/en/latest/?badge=latest"
        img = f"readthedocs.org/projects/{project}/badge/?version=latest"
        badge = fmt_badge(img, url, "Documentation status", cfg['doc']['fmt'])

        return {"badge": badge}
