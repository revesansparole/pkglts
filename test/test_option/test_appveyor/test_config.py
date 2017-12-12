from pkglts.config_management import Config
from pkglts.option.appveyor.config import check, require, update_parameters


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['appveyor']) == 1


def test_config_does_nothing():
    cfg = Config(dict(appveyor={'token': 'toto'}))
    assert len(check(cfg)) == 0


def test_require():
    cfg = Config(dict(base={}, travis={}))
    
    assert len(require('option', cfg)) == 2
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
