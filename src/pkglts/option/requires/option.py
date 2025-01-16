import logging
from pathlib import Path

from pkglts.option.doc.badge import Badge
from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionRequires(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self, cfg):
        return ["doc", "github"]

    def environment_extensions(self, cfg):
        owner = cfg["github"]["owner"]
        project = cfg["github"]["project"]

        base_url = f"requires.io/github/{owner}/{project}/"
        url = f"{base_url}requirements/?branch=master"
        img = f"{base_url}requirements.svg?branch=master"
        badge = Badge(name="requires", url=url, url_img=img, text="Requirements status")

        return {"badge": badge}
