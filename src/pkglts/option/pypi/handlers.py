from pkglts.local import pkg_full_name
from pkglts.option.doc import fmt_badge


def auto_classifiers(env):
    items = set(env.globals['pypi'].classifiers)

    # add license item
    # TODO

    # add intended versions items
    intended_versions = env.globals['pysetup'].intended_versions
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


def environment_extensions(env):
    """Add more functionality to an environment.

    Args:
        env (jinja2.Environment):

    Returns:
        dict of str: any
    """
    url = "badge.fury.io/py/%s" % pkg_full_name(env)
    img = url + ".svg"
    badge = fmt_badge(img, url, "PyPI version")

    return {"badge": badge,
            "auto_classifiers": auto_classifiers(env)}
