from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.local import pkg_full_name
from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option


class OptionPypi(Option):
    def root_dir(self):
        return dirname(__file__)

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
        cfg['pypi'] = sec

    def check(self, cfg):
        invalids = []
        classifiers = cfg['pypi']['classifiers']

        if not classifiers:
            invalids.append("pypi.classifiers")

        return invalids

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['doc', 'pysetup']
            return [Dependency(name) for name in options]

        if purpose == 'dvlpt':
            return [Dependency('twine', pkg_mng='pip')]

        return []

    def environment_extensions(self, cfg):
        servers = cfg['pypi']['servers']
        if servers and servers[0]['name'] == 'pypi':
            url = "badge.fury.io/py/%s" % pkg_full_name(cfg)
            img = url + ".svg"
            badge = fmt_badge(img, url, "PyPI version", cfg['doc']['fmt'])
        else:
            badge = ""

        return {"badge": badge,
                "auto_classifiers": auto_classifiers(cfg)}


def auto_classifiers(cfg):
    """Generate a list of calssifiers for pypi from all sections of config.

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
