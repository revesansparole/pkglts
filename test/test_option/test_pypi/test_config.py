from pkglts.config_management import create_env
from pkglts.option.pypi.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 1


def test_config_check_classifiers_exists():
    env = create_env(dict(pypi={'classifiers': []}))
    assert 'classifiers' in check(env)


def test_require():
    cfg = dict(pypi={})
    env = create_env(cfg)

    assert len(require('option', env)) == 1
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 1
