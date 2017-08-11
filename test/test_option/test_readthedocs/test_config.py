from pkglts.config_management import Config
from pkglts.option.readthedocs.config import check, require, update_parameters


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['readthedocs']) == 1


def test_config_check_project_exists():
    cfg = Config(dict(readthedocs={'project': ""}))
    assert 'readthedocs.project' in check(cfg)


def test_require():
    cfg = Config(dict(readthedocs={}))

    assert len(require('option', cfg)) == 3
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
