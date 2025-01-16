import logging
from pathlib import Path

from pkglts.dependency import Dependency
from pkglts.local import pkg_full_name
from pkglts.option.doc.badge import Badge
from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionPypi(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        LOGGER.info("update parameters %s", self._name)
        sec = dict(
            classifiers=[
                "Development Status :: 2 - Pre-Alpha",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: BSD License",
                "Natural Language :: English",
            ],
            servers=[
                dict(name="pypi", url="https://upload.pypi.org/legacy/"),
                dict(name="test", url="https://testpypi.python.org/pypi"),
            ],
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        classifiers = cfg[self._name]["classifiers"]

        if not classifiers:
            invalids.append("pypi.classifiers")

        return invalids

    def require_option(self, cfg):
        return ["doc", "pyproject"]

    def require(self, cfg):
        del cfg
        yield Dependency("twine", intent="dvlpt")

    def environment_extensions(self, cfg):
        ext = {"auto_classifiers": auto_classifiers(cfg)}

        servers = cfg["pypi"]["servers"]
        if servers and servers[0]["name"] == "pypi":
            url = f"badge.fury.io/py/{pkg_full_name(cfg)}"
            ext["badge"] = Badge(name="pypi", url=url, url_img=f"{url}.svg", text="PyPI version")

        return ext


def auto_classifiers(cfg):
    """Generate a list of classifiers for pypi from all sections of config.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str)
    """
    items = set(cfg["pypi"]["classifiers"])

    # add license item
    # TODO

    # add intended versions items
    intended_versions = cfg["pyproject"]["intended_versions"]
    if intended_versions:
        items.add("Programming Language :: Python")

        ver_cla_tpl = "Programming Language :: Python :: {}"
        major_versions = set()
        for ver in intended_versions:
            items.add(ver_cla_tpl.format(ver))
            major_versions.add(ver.split(".")[0])

        for ver in major_versions:
            items.add(ver_cla_tpl.format(ver))

        if len(major_versions) == 1:
            (ver,) = major_versions
            items.add(f"Programming Language :: Python :: {ver} :: Only")

    return sorted(items)
