from pkglts.option.readthedocs.handlers import badge, mapping


def test_handlers():
    assert len(mapping) == 1


def test_badge():
    pkg_cfg = dict(base={'pkgname': "pkg", 'owner': "moi"},
                   github={'project': "project"})
    assert ".. image:" in badge("txt", pkg_cfg)
