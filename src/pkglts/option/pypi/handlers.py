from pkglts.option.doc import fmt_badge


def badge(txt, env):
    del txt  # unused
    pkgname = env['base']['pkgname']

    url = "badge.fury.io/py/%s" % pkgname
    img = url + ".svg"
    return fmt_badge(img, url, "PyPI version")


def get_classifiers(txt, env):
    del txt  # unused

    items = list(env['pypi']['classifiers'])

    # add license item
    # TODO

    # add intended versions items
    intended_versions = env['pysetup']['intended_versions']
    if len(intended_versions) > 0:
        items.append("Programming Language :: Python")

        ver_cla_tpl = "Programming Language :: Python :: %s.%s"
        major_versions = set()
        for ver in intended_versions:
            items.append(ver_cla_tpl % (ver[0], ver[1]))
            major_versions.add(ver[0])

        ver_cla_tpl = "Programming Language :: Python :: %s"
        for ver in major_versions:
            items.append(ver_cla_tpl % ver)

        if len(major_versions) == 1:
            ver, = major_versions
            items.append("Programming Language :: Python :: %s :: Only" % ver)

    return "\n" + ",\n".join(" " * 8 + "'%s'" % it for it in sorted(items))


mapping = {'pypi.badge': badge,
           'pypi.classifiers': get_classifiers}
