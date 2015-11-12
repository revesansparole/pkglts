from pkglts.option.doc import fmt_badge


def badge(txt, env):
    del txt  # unused
    pkgname = env['base']['pkgname']

    url = "badge.fury.io/py/%s" % pkgname
    img = url + ".svg"
    return fmt_badge(img, url, "PyPI version")


def get_classifiers(txt, env):
    del txt  # unused
    cfg = env['pysetup']

    items = [" " * 8 + "'%s'," % key for key in cfg['classifiers']]

    # add license item
    # TODO

    # add intended versions items
    ver_cla_tpl = " " * 8 + "'Programming Language :: Python :: %s.%s',"
    for ver in cfg['intended_versions']:
        items.append(ver_cla_tpl % (ver[0], ver[1]))

    return "\n" + "\n".join(items)


mapping = {'pypi.badge': badge,
           'pypi.classifiers': get_classifiers}
