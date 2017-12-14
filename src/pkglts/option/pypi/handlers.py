"""
Set of function to extend jinja2 environment.
"""
from pkglts.local import pkg_full_name
from pkglts.option.doc import fmt_badge


def auto_classifiers(cfg):
    items = set(cfg['pypi']['classifiers'])

    # add license item
    # TODO

    # add intended versions items
    intended_versions = cfg['pysetup']['intended_versions']
    if len(intended_versions) > 0:
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


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    url = "badge.fury.io/py/%s" % pkg_full_name(cfg)
    img = url + ".svg"
    badge = fmt_badge(img, url, "PyPI version", cfg['doc']['fmt'])

    return {"badge": badge,
            "auto_classifiers": auto_classifiers(cfg)}
