from pkglts.config_management import Config
from pkglts.option.git.config import check, require, update_parameters


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['git']) == 0


def test_config_check_nothing():
    cfg = Config(dict(git={}))
    assert len(check(cfg)) == 0


def test_require():
    cfg = Config(dict(base={}, data={}))

    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
