from pkglts.config_management import create_env
from pkglts.option.plugin.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 0


def test_config_check_sphinx_theme():
    env = create_env(dict(plugin={'tugudu': 'poutou'}))
    assert len(check(env)) == 0


def test_require():
    cfg = dict(plugin={})
    env = create_env(cfg)

    assert len(require('option', env)) == 0
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 1
