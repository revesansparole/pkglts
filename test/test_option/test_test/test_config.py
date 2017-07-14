from pkglts.config_management import Config
from pkglts.option.test.config import check, require, update_parameters


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['test']) == 1


def test_config_check_suite_names():
    for name in ('walou', ' nose'):
        cfg = Config(dict(test={'suite_name': name}))
        assert 'suite_name' in check(cfg)


def test_require():
    for suite_name in ('pytest', 'nose'):
        cfg = Config(dict(base={}, test={'suite_name': suite_name}))

        assert len(require('option', cfg)) == 1
        assert len(require('setup', cfg)) == 0
        assert len(require('install', cfg)) == 0
        assert len(require('dvlpt', cfg)) == 2
