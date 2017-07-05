from pkglts.config_management import create_env
from pkglts.option.license.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 4


def test_config_check_license_name_exists():
    env = create_env(dict(license={'name': "", 'year': 2015,
                                   'organization': "oa", 'project': "project"}))
    assert 'name' in check(env)

    env = create_env(dict(license={'name': "tugudu", 'year': 2015,
                                   'organization': "oa", 'project': "project"}))
    assert 'name' in check(env)


def test_require():
    cfg = dict(license={})
    env = create_env(cfg)

    assert len(require('option', env)) == 1
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 0
