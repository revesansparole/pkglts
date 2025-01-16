import logging
from pathlib import Path

from pkglts.option.doc.badge import Badge
from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionLgtm(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self, cfg):
        return ["github", "pyproject"]

    def environment_extensions(self, cfg):
        owner = cfg["github"]["owner"]
        project = cfg["github"]["project"]

        url = f"https://lgtm.com/projects/g/{owner}/{project}/context:python"
        img = f"https://img.shields.io/lgtm/grade/python/g/{owner}/{project}.svg?logo=lgtm&logoWidth=18"
        badge = Badge(name="lgtm", url=url, url_img=img, text="Language grade: Python")

        return {"badge": badge}
