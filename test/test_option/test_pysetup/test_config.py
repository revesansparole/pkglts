from pkglts.config_management import create_env
from pkglts.option.pysetup.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 2


def test_config_check_intended_version_exists():
    env = create_env(dict(pysetup={'intended_versions': [], 'require': []}))
    assert 'intended_versions' in check(env)
    assert 'require' not in check(env)

    env = create_env(dict(pysetup={'intended_versions': ["27"],
                                   'require': [('walou', 'numpy')]}))
    assert 'require' in check(env)


def test_require():
    cfg = dict(test={},
               pysetup={'intended_versions': ["27"],
                        'require': []})
    env = create_env(cfg)

    assert len(require('option', env)) == 5
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 0
