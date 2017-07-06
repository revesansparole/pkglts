from pkglts.config_management import create_env
from pkglts.option.readthedocs.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 1


def test_config_check_project_exists():
    env = create_env(dict(readthedocs={'project': ""}))
    assert 'project' in check(env)


def test_require():
    cfg = dict(readthedocs={})
    env = create_env(cfg)

    assert len(require('option', env)) == 3
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 0
