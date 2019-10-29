from pathlib import Path

from pkglts.dependency import Dependency
from pkglts.local import pkg_full_name
from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionPypi(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        sec = dict(
            classifiers=[
                "Development Status :: 2 - Pre-Alpha",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: BSD License",
                "Natural Language :: English"
            ],
            servers=[
                dict(name="pypi", url="https://upload.pypi.org/legacy/"),
                dict(name="test", url="https://testpypi.python.org/pypi")
            ]
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        classifiers = cfg[self._name]['classifiers']

        if not classifiers:
            invalids.append("pypi.classifiers")

        return invalids

    def require_option(self):
        return ['doc', 'pysetup']

    def require(self, cfg):
        del cfg
        yield Dependency('twine', intent='dvlpt')

    def environment_extensions(self, cfg):
        servers = cfg['pypi']['servers']
        if servers and servers[0]['name'] == 'pypi':
            url = f"badge.fury.io/py/{pkg_full_name(cfg)}"
            img = f"{url}.svg"
            badge = fmt_badge(img, url, "PyPI version", cfg['doc']['fmt'])
        else:
            badge = ""

        return {"badge": badge,
                "auto_classifiers": auto_classifiers(cfg)}


def auto_classifiers(cfg):
    """Generate a list of classifiers for pypi from all sections of config.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str)
    """
    items = set(cfg['pypi']['classifiers'])

    # add license item
    # TODO

    # add intended versions items
    intended_versions = cfg['pysetup']['intended_versions']
    if intended_versions:
        items.add("Programming Language :: Python")

        ver_cla_tpl = "Programming Language :: Python :: %s.%s"
        major_versions = set()
        for ver in intended_versions:
            items.add(ver_cla_tpl % (ver[0], ver[1]))
            major_versions.add(ver[0])

        ver_cla_tpl = "Programming Language :: Python :: %s"
        for ver in major_versions:
            items.add(ver_cla_tpl % ver)

        if len(major_versions) == 1:
            ver, = major_versions
            items.add("Programming Language :: Python :: %s :: Only" % ver)

    return sorted(items)
