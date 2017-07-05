from pkglts.config_management import create_env
from pkglts.option.sphinx.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 2


def test_config_check_sphinx_theme():
    for theme in (1, None,):
        env = create_env(dict(sphinx={'theme': theme}))
        assert 'theme' in check(env)


def test_require():
    cfg = dict(sphinx={})
    env = create_env(cfg)

    assert len(require('option', env)) == 2
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 1
