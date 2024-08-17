import logging
from pathlib import Path

from pkglts.option.reqs.option import requirements
from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionConda(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        LOGGER.info("update parameters %s", self._name)
        sec = dict(
            env_name="{{ base.pkgname }}",
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        env_name = cfg[self._name]['env_name']

        if not env_name:
            invalids.append("conda.env_name")

        if len(env_name) != len(env_name.strip()) or "-" in env_name:
            invalids.append("conda.env_name")

        return invalids

    def require_option(self, cfg):
        return ['pyproject']

    def environment_extensions(self, cfg):
        channels = [dep.channel for dep in requirements(cfg) if dep.channel is not None]
        channels_minimal = [dep.channel for dep in requirements(cfg)
                            if 'install' in dep.intents and dep.channel is not None]

        return {"channels": channels, "channels_minimal": channels_minimal}
