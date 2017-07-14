from pkglts.config_management import Config
from pkglts.option.pypi.config import check, require, update_parameters


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['pypi']) == 1


def test_config_check_classifiers_exists():
    cfg = Config(dict(pypi={'classifiers': []}))
    assert 'classifiers' in check(cfg)


def test_require():
    cfg = Config(dict(pypi={}))

    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 1
