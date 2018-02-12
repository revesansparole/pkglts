"""
Set of function to extend jinja2 environment.
"""
from pkglts.local import pkg_full_name
from pkglts.option.doc import fmt_badge


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


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    servers = cfg['pypi']['servers']
    if servers and servers[0]['name'] == 'pypi':
        url = "badge.fury.io/py/%s" % pkg_full_name(cfg)
        img = url + ".svg"
        badge = fmt_badge(img, url, "PyPI version", cfg['doc']['fmt'])
    else:
        badge = ""

    return {"badge": badge,
            "auto_classifiers": auto_classifiers(cfg)}
