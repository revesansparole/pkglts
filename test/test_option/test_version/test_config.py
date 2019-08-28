import pytest
from pkglts.config_management import Config
from pkglts.option.version.option import OptionVersion


@pytest.fixture()
def opt():
    return OptionVersion('version')


def test_version_is_defined(opt):
    assert opt.version() != "0.0.0"


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['version']) == 3


def test_config_check_version_numbers_are_valid(opt):
    cfg = Config(dict(version={'major': "", 'minor': "", 'post': ""}))
    assert 'version.major' in opt.check(cfg)
    assert 'version.minor' in opt.check(cfg)
    assert 'version.post' in opt.check(cfg)
    cfg = Config(dict(version={'major': "a", 'minor': "a", 'post': "a"}))
    assert 'version.major' in opt.check(cfg)
    assert 'version.minor' in opt.check(cfg)
    assert 'version.post' in opt.check(cfg)
    cfg = Config(dict(version={'major': "1", 'minor': "1", 'post': "1"}))
    assert 'version.major' in opt.check(cfg)
    assert 'version.minor' in opt.check(cfg)
    assert 'version.post' in opt.check(cfg)
    cfg = Config(dict(version={'major': 1, 'minor': 0, 'post': "2.dev"}))
    assert 'version.post' in opt.check(cfg)


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
