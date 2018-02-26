import pytest
from pkglts.config_management import Config
from pkglts.option.base.option import OptionBase


@pytest.fixture()
def opt():
    return OptionBase('base')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['base']) == 5


def test_config_check_pkg_names(opt):
    for pkg in ('1mypkg', ' mypkg', '1', '1.mypkg',
                ' .mypkg', '.mypkg', 'None.mypkg', 'oa.o.mypkg'):
        cfg = Config(dict(base={'pkgname': pkg,
                                'namespace': None,
                                'namespace_method': "pkg_util",
                                'owner': 'moi',
                                'url': None}))
        assert 'base.pkgname' in opt.check(cfg)
        cfg = Config(dict(base={'pkgname': 'toto',
                                'namespace': pkg,
                                'namespace_method': "pkg_util",
                                'owner': 'moi',
                                'url': None}))
        assert 'base.namespace' in opt.check(cfg)

    cfg = Config(dict(base={'pkgname': 'toto',
                            'namespace': None,
                            'namespace_method': "toto",
                            'owner': 'moi',
                            'url': None}))
    assert 'base.namespace_method' in opt.check(cfg)


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(opt.require('option', cfg)) == 0
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 0
    assert len(opt.require('dvlpt', cfg)) == 0
