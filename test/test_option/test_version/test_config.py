from pkglts.config_management import create_env
from pkglts.option.version.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 3


def test_config_check_version_numbers_are_valid():
    env = create_env(dict(version={'major': "", 'minor': "", 'post': ""}))
    assert 'major' in check(env)
    assert 'minor' in check(env)
    assert 'post' in check(env)
    env = create_env(dict(version={'major': "a", 'minor': "a", 'post': "a"}))
    assert 'major' in check(env)
    assert 'minor' in check(env)
    assert 'post' in check(env)
    env = create_env(dict(version={'major': "1", 'minor': "1", 'post': "1"}))
    assert 'major' in check(env)
    assert 'minor' in check(env)
    assert 'post' in check(env)
    env = create_env(dict(version={'major': 1, 'minor': 0, 'post': "2.dev"}))
    assert 'post' in check(env)


def test_require():
    cfg = dict(base={}, version={})
    env = create_env(cfg)

    assert len(require('option', env)) == 1
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 0
