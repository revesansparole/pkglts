import logging
from pathlib import Path

from url_normalize import url_normalize

from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionPyproject(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        LOGGER.info("update parameters %s", self._name)
        sec = dict(
            intended_versions=["3.11"],
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        intended_versions = cfg[self._name]['intended_versions']

        if not intended_versions:
            invalids.append("pyproject.intended_versions")

        return invalids

    def require_option(self, cfg):
        return ['src', 'doc', 'license', 'version', 'reqs']

    def environment_extensions(self, cfg):
        py_vers = sorted([int(v) for v in ver.split(".")] for ver in cfg[self._name]['intended_versions'])

        universal = len(set(ver.split(".")[0] for ver in cfg[self._name]['intended_versions'])) > 1

        return {
            "urls": find_urls(cfg),
            "py_max_ver": ".".join(str(v) for v in py_vers[-1]),
            "py_min_ver": ".".join(str(v) for v in py_vers[0]),
            "universal": universal
        }


def find_urls(cfg):
    """Extract all valid urls from all config sections.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict(str, str): key, url
    """
    urls = {}
    for name, section, key in [
        ("homepage", "base", "url"),
        ("repository", "github", "url"),
        ("repository", "gitlab", "url"),
    ]:
        try:
            url = cfg[section][key]
            if url is not None:
                urls[name] = url_normalize(url)
        except KeyError:
            pass

    return urls
