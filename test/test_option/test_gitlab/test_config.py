from pkglts.config_management import Config
from pkglts.option.gitlab.config import check, require, update_parameters


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['gitlab']) == 3


def test_config_check_project_exists():
    cfg = Config(dict(gitlab={'owner': "", 'project': "", "url": ""}))
    assert 'gitlab.project' in check(cfg)


def test_require():
    cfg = Config(dict(base={}, data={}))

    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
