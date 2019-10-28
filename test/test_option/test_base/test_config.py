import pytest
from pkglts.config_management import Config
from pkglts.option.base.option import OptionBase


@pytest.fixture()
def opt():
    return OptionBase('base')


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['base']) == 4


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


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 0


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
