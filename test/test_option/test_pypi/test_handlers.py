from pkglts.option.pypi.handlers import mapping, get_classifiers


def test_handlers():
    assert len(mapping) == 1


def test_get_classifiers():
    pkg_cfg = dict(pydist={'intended_versions': [], 'classifiers': []})
    assert get_classifiers("txt", pkg_cfg) == "\n"


def test_get_classifiers_find_version_classifiers():
    pkg_cfg = dict(pydist={'intended_versions': ["27"], 'classifiers': []})
    assert len(get_classifiers("txt", pkg_cfg).split("\n")) == 2
