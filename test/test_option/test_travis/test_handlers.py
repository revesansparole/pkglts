from pkglts.option.travis.handlers import badge, mapping, pyversions


def test_mapping():
    assert len(mapping) == 2


def test_handlers():
    pkg_cfg = dict(setup={'intended_versions': ["27"]})
    txt = pyversions("txt", pkg_cfg)
    assert txt != "txt"


def test_badge():
    pkg_cfg = dict(base={'pkgname': "pkg", 'owner': "moi"},
                   github={'project': "project"})
    assert ".. image:" in badge("txt", pkg_cfg)
