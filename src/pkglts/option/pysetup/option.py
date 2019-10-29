from pathlib import Path

from pkglts.option_object import Option
from pkglts.version import __version__


class OptionPysetup(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        sec = dict(
            intended_versions=["36"],
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        intended_versions = cfg[self._name]['intended_versions']

        if not intended_versions:
            invalids.append("pysetup.intended_versions")

        return invalids

    def require_option(self):
        return ['src', 'doc', 'license', 'version', 'reqs']

    def environment_extensions(self, cfg):
        return {
            "pkg_url": pkg_url(cfg),
        }


def pkg_url(cfg):
    """Extract a valid url from all config sections.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (str): a valid url for the package
    """
    try:
        url = cfg['base']['url']
        if url is not None:
            return url
    except KeyError:
        pass

    try:
        url = cfg['github']['url']
        if url is not None:
            return url
    except KeyError:
        pass

    try:
        url = cfg['gitlab']['url']
        if url is not None:
            return url
    except KeyError:
        pass

    # try:
    #     url = cfg['pypi']['url']
    #     if url is not None:
    #         return url
    # except KeyError:
    #     pass

    # try:
    #     url = cfg['readthedocs']['url']
    #     if url is not None:
    #         return url
    # except KeyError:
    #     pass

    return ""
