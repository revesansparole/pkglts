from pkglts.config_management import Config
from pkglts.option.doc.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 2


def test_config_check_description_exists():
    cfg = Config(dict(doc={'description': "mydescr", 'keywords': []}))
    assert cfg['doc']['description'] == "mydescr"
    assert 'description' not in check(cfg)


def test_config_check_description_valid():
    cfg = Config(dict(doc={'description': "", 'keywords': []}))
    assert 'description' in check(cfg)


def test_config_check_keywords_exists():
    cfg = Config(dict(doc={'description': "mydescr", 'keywords': []}))
    assert len(cfg['doc']['keywords']) == 0
    assert 'keywords' not in check(cfg)


def test_require():
    cfg = Config(dict(base={}, doc={}))

    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
