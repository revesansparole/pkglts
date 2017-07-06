from pkglts.config_management import create_env
from pkglts.option.github.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 3


def test_config_check_project_exists():
    env = create_env(dict(github={'owner': "", 'project': "", "url": ""}))
    assert 'project' in check(env)


def test_require():
    cfg = dict(base={}, data={})
    env = create_env(cfg)

    assert len(require('option', env)) == 1
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 0
