import pytest
from pkglts.config_management import Config
from pkglts.option.version.option import OptionVersion


@pytest.fixture()
def opt():
    return OptionVersion('version')


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg['version']) == 3


def test_config_check_version_numbers_are_valid(opt, cfg):
    cfg['version'] = {'major': "", 'minor': "", 'post': ""}
    assert 'version.major' in opt.check(cfg)
    assert 'version.minor' in opt.check(cfg)
    assert 'version.post' in opt.check(cfg)
    cfg['version'] = {'major': "a", 'minor': "a", 'post': "a"}
    assert 'version.major' in opt.check(cfg)
    assert 'version.minor' in opt.check(cfg)
    assert 'version.post' in opt.check(cfg)
    cfg['version'] = {'major': "1", 'minor': "1", 'post': "1"}
    assert 'version.major' in opt.check(cfg)
    assert 'version.minor' in opt.check(cfg)
    assert 'version.post' in opt.check(cfg)
    cfg['version'] = {'major': 1, 'minor': 0, 'post': "2.dev"}
    assert 'version.post' in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
