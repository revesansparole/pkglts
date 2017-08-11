from pkglts.config_management import Config
from pkglts.option.doc.config import check, require, update_parameters


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['doc']) == 3


def test_config_check_description_exists():
    cfg = Config(dict(doc={'description': "mydescr", 'fmt': 'rst', 'keywords': []}))
    assert cfg['doc']['description'] == "mydescr"
    assert 'doc.description' not in check(cfg)


def test_config_check_description_valid():
    cfg = Config(dict(doc={'description': "", 'fmt': 'rst', 'keywords': []}))
    assert 'doc.description' in check(cfg)


def test_config_check_keywords_exists():
    cfg = Config(dict(doc={'description': "mydescr", 'fmt': 'rst', 'keywords': []}))
    assert len(cfg['doc']['keywords']) == 0
    assert 'doc.keywords' not in check(cfg)


def test_config_check_fmt_valid():
    cfg = Config(dict(doc={'description': "mydescr", 'fmt': 'walou', 'keywords': []}))
    assert 'fmt' in check(cfg)


def test_config_check_fmt_valid():
    cfg = Config(dict(doc={'description': "mydescr", 'fmt': 'walou', 'keywords': []}))
    assert 'fmt' in check(cfg)


def test_require():
    cfg = Config(dict(base={}, doc={}))
    
    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
