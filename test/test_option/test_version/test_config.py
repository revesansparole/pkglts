from pkglts.config_managment import create_env
from pkglts.option.version.config import check, parameters


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
