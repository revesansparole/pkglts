import logging
from pathlib import Path

from pkglts.option.doc.badge import Badge
from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionLandscape(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self, cfg):
        return ["flake8", "travis"]

    def environment_extensions(self, cfg):
        owner = cfg["github"]["owner"]
        project = cfg["github"]["project"]

        url = f"landscape.io/github/{owner}/{project}/master"
        img = f"{url}/landscape.svg?style=flat"
        badge = Badge(name="landscape", url=url, url_img=img, text="Code health status")

        return {"badge": badge}
