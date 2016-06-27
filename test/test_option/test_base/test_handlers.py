from pkglts.config_management import pkg_env


def test_src_pth():
    env = pkg_env({'base': {'pkgname': 'toto', 'namespace': None}})
    assert env.globals['base'].src_pth == "src/toto"
    env = pkg_env({'base': {'pkgname': 'toto', 'namespace': 'oa'}})
    assert env.globals['base'].src_pth == "src/oa/toto"


def test_pkg_full_name():
    env = pkg_env({'base': {'pkgname': 'toto', 'namespace': None}})
    assert env.globals['base'].pkg_full_name == "toto"
    env = pkg_env({'base': {'pkgname': 'toto', 'namespace': 'oa'}})
    assert env.globals['base'].pkg_full_name == "oa.toto"
