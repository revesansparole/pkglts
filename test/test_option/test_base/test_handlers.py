from pkglts.config_management import Config


def test_src_pth():
    cfg = Config({'base': {'pkgname': 'toto', 'namespace': None}})
    cfg.load_extra()
    assert cfg._env.globals['base'].src_pth == "src/toto"
#     cfg = Config({'base': {'pkgname': 'toto', 'namespace': 'oa'}})
#     cfg.load_extra()
#     assert cfg._env.globals['base'].src_pth == "src/oa/toto"
#
#
# def test_pkg_full_name():
#     cfg = Config({'base': {'pkgname': 'toto', 'namespace': None}})
#     cfg.load_extra()
#     assert cfg._env.globals['base'].pkg_full_name == "toto"
#     cfg = Config({'base': {'pkgname': 'toto', 'namespace': 'oa'}})
#     cfg.load_extra()
#     assert cfg._env.globals['base'].pkg_full_name == "oa.toto"
