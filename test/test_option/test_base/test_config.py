from pkglts.config_management import Config
from pkglts.option.base.config import check, require, update_parameters


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['base']) == 5


def test_config_check_pkg_names():
    for pkg in ('1mypkg', ' mypkg', '1', '1.mypkg',
                ' .mypkg', '.mypkg', 'None.mypkg', 'oa.o.mypkg'):
        cfg = Config(dict(base={'pkgname': pkg,
                                    'namespace': None,
                                    'namespace_method': "pkg_util",
                                    'owner': 'moi',
                                    'url': None}))
        assert 'pkgname' in check(cfg)
        cfg = Config(dict(base={'pkgname': 'toto',
                                    'namespace': pkg,
                                    'namespace_method': "pkg_util",
                                    'owner': 'moi',
                                    'url': None}))
        assert 'namespace' in check(cfg)

    cfg = Config(dict(base={'pkgname': 'toto',
                                'namespace': None,
                                'namespace_method': "toto",
                                'owner': 'moi',
                                'url': None}))
    assert 'namespace_method' in check(cfg)


def test_require():
    cfg = Config(dict(base={}))

    assert len(require('option', cfg)) == 0
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
