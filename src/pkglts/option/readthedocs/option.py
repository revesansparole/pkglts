import logging
from pathlib import Path

from pkglts.option.doc.badge import Badge
from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionReadthedocs(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        LOGGER.info("update parameters %s", self._name)
        if "gitlab" in cfg:
            prj_name = "{{ gitlab.project }}"
        elif "github" in cfg:
            prj_name = "{{ github.project }}"
        else:
            raise NotImplementedError("not supposed to happen")

        sec = dict(project=prj_name)
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        project = cfg[self._name]["project"]

        if not project:
            invalids.append("readthedocs.project")

        return invalids

    def require_option(self, cfg):
        reqs = ["pyproject", "sphinx"]
        if "gitlab" in cfg:
            reqs.append("gitlab")
        elif "github" in cfg:
            reqs.append("github")
        else:
            raise UserWarning("need either github or gitlab and don't want to decide for you")

        return reqs

    def environment_extensions(self, cfg):
        project = cfg["readthedocs"]["project"]
        project = project.replace(".", "")
        url = f"{project}.readthedocs.io/en/latest/?badge=latest"
        img = f"readthedocs.org/projects/{project}/badge/?version=latest"
        badge = Badge(name="readthedocs", url=url, url_img=img, text="Documentation status")

        return {"badge": badge}
