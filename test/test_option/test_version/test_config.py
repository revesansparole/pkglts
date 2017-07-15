from pkglts.config_management import Config
from pkglts.option.version.config import check, require, update_parameters


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['version']) == 3


def test_config_check_version_numbers_are_valid():
    cfg = Config(dict(version={'major': "", 'minor': "", 'post': ""}))
    assert 'major' in check(cfg)
    assert 'minor' in check(cfg)
    assert 'post' in check(cfg)
    cfg = Config(dict(version={'major': "a", 'minor': "a", 'post': "a"}))
    assert 'major' in check(cfg)
    assert 'minor' in check(cfg)
    assert 'post' in check(cfg)
    cfg = Config(dict(version={'major': "1", 'minor': "1", 'post': "1"}))
    assert 'major' in check(cfg)
    assert 'minor' in check(cfg)
    assert 'post' in check(cfg)
    cfg = Config(dict(version={'major': 1, 'minor': 0, 'post': "2.dev"}))
    assert 'post' in check(cfg)


def test_require():
    cfg = Config(dict(base={}, version={}))

    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
