from pkglts.option.pypi.handlers import badge, mapping, get_classifiers


def test_handlers():
    assert len(mapping) == 2


def test_get_classifiers():
    pkg_cfg = dict(pysetup={'intended_versions': []}, pypi={'classifiers': []})
    assert get_classifiers("txt", pkg_cfg) == "\n"


def test_get_classifiers_find_version_classifiers():
    pkg_cfg = dict(pysetup={'intended_versions': ["27", "34"]},
                   pypi={'classifiers': []})
    assert len(get_classifiers("txt", pkg_cfg).split("\n")) == 6


def test_badge():
    pkg_cfg = dict(base={'pkgname': "pkg", 'namespace': None, 'owner': "moi"},
                   github={'project': "project"})
    assert ".. image:" in badge("txt", pkg_cfg)
