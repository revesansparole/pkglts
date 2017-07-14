from pkglts.config_management import Config
from pkglts.option.pysetup.config import check, require, update_parameters


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['pysetup']) == 2


def test_config_check_intended_version_exists():
    cfg = Config(dict(pysetup={'intended_versions': [], 'require': []}))
    assert 'intended_versions' in check(cfg)
    assert 'require' not in check(cfg)

    cfg = Config(dict(pysetup={'intended_versions': ["27"],
                               'require': [{'pkg_mng': 'walou', 'name': 'numpy'}]}))
    assert 'require' in check(cfg)


def test_require():
    cfg = Config(dict(test={},
                      pysetup={'intended_versions': ["27"],
                               'require': []}))

    assert len(require('option', cfg)) == 5
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
