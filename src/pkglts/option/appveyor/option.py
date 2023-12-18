import logging
from pathlib import Path

from pkglts.option.doc.badge import Badge
from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionAppveyor(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        LOGGER.info("update parameters %s", self._name)
        sec = dict(
            token=""
        )
        cfg[self._name] = sec

    def require_option(self, cfg):
        return ['doc', 'pyproject', 'github']

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project'].replace("_", "-")
        token = cfg[self._name]['token']

        url = f"ci.appveyor.com/project/{owner}/{project}/branch/master"
        img = f"ci.appveyor.com/api/projects/status/{token}/branch/master?svg=true"
        badge = Badge(
            name="appveyor",
            url=url,
            url_img=img,
            text="Appveyor build status"
        )

        return {"badge": badge}
