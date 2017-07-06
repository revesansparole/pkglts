import pytest

from pkglts.config_management import pkg_env


def test_generate():
    cfg = dict(name='mit',
               year="2015",
               organization="org",
               project="project")
    env = pkg_env(dict(license=cfg))
    assert len(env.globals['license'].full_text) > 0


def test_generate_raise_error_if_license_do_not_exists():
    cfg = dict(name='tugudu',
               year="2015",
               organization="org",
               project="project")
    with pytest.raises(IOError):
        pkg_env(dict(license=cfg))
