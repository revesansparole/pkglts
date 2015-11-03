from pkglts.option.doc.handlers import badges


def test_badges():
    assert badges("txt", {}) == "txt"


def test_badges_number():
    pkg_cfg = dict(base=dict(owner='toto', pkgname='pkgname'),
                   github=dict(project='project'))
    txt = badges("txt", pkg_cfg)
    assert txt == "txt"

    web_services = ("readthedocs", "travis", "coveralls", "landscape", "pypi")
    for name in web_services:
        pkg_cfg[name] = {}

    txt = badges("txt", pkg_cfg)
    assert txt.count(".. image::") == len(web_services)
