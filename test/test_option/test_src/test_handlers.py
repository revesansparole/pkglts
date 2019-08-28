from pkglts.config_management import Config


def test_src_pth():
    cfg = Config({
        'base': {'pkgname': 'toto', 'namespace': None},
        'src': {'namespace_method': 'pkg_util'}
    })
    cfg.load_extra()
    assert cfg._env.globals['src'].src_pth == "src/toto"
