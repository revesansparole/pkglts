from nose.tools import assert_raises

from pkglts.option.pydist.handlers import mapping, requirements, get_url

# TODO get_extra

def test_handlers():
    assert len(mapping) == 3


def test_requirements():
    pkg_cfg = {}
    assert requirements("txt", pkg_cfg) == ""


def test_requirements_error_for_bad_options():
    pkg_cfg = {'toto': {}}
    assert_raises(KeyError, lambda: requirements("txt", pkg_cfg))


def test_get_requirements_get_install_requirements():
    pkg_cfg = {'test': {}}
    assert requirements("txt", pkg_cfg) == "nose\nmock"


def test_get_url_return_empty_default():
    pkg_cfg = {}
    assert get_url("txt", pkg_cfg) == ""


# TODO bug corrections self referencing tests
def test_get_url_return_base_url():
    pkg_cfg = dict(base={'url': 'base'})
    assert get_url("txt", pkg_cfg) == "base"
    pkg_cfg["github"] = {'url': 'github'}
    assert get_url("txt", pkg_cfg) == "base"
    pkg_cfg["base"]['url'] = None
    assert get_url("txt", pkg_cfg) == "github"


def test_get_url_look_multiple_places():
    for name in ("base", "github", "pypi", "readthedocs"):
        pkg_cfg = {name: {'url': name}}
        assert get_url("txt", pkg_cfg) == name


def test_get_url_avoid_none_urls():
    places = ("base", "github", "pypi", "readthedocs")
    for name in places:
        pkg_cfg = dict((n, {'url': None}) for n in places)
        pkg_cfg[name]['url'] = name
        assert get_url("txt", pkg_cfg) == name
