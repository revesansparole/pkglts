from pkglts.config_management import create_env
from pkglts.option.test.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 1


def test_config_check_suite_names():
    for name in ('walou', ' nose'):
        env = create_env(dict(test={'suite_name': name}))
        assert 'suite_name' in check(env)


def test_require():
    for suite_name in ('pytest', 'nose'):
        cfg = dict(base={}, test={'suite_name': suite_name})
        env = create_env(cfg)

        assert len(require('option', env)) == 1
        assert len(require('setup', env)) == 0
        assert len(require('install', env)) == 0
        assert len(require('dvlpt', env)) == 2
