import logging
from pathlib import Path

from pkglts.option.doc.badge import Badge
from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionTravis(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self, cfg):
        return ["doc", "pyproject", "github"]

    def environment_extensions(self, cfg):
        owner = cfg["github"]["owner"]
        project = cfg["github"]["project"]

        url = f"travis-ci.com/github/{owner}/{project}"
        img = f"api.travis-ci.com/{owner}/{project}.svg?branch=master"
        badge = Badge(name="travis", url=url, url_img=img, text="Travis build status")

        return {"badge": badge}
