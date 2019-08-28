import pytest
from pkglts.config_management import Config
from pkglts.option.src.option import OptionSrc


@pytest.fixture()
def opt():
    return OptionSrc('src')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['src']) == 1


def test_config_check_pkg_names(opt):
    cfg = Config(dict(src={'namespace_method': "toto"}))
    assert 'src.namespace_method' in opt.check(cfg)


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
