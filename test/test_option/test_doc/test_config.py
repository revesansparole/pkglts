import pytest
from pkglts.config_management import Config
from pkglts.option.doc.option import OptionDoc


@pytest.fixture()
def opt():
    return OptionDoc('doc')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['doc']) == 3


def test_config_check_description_exists(opt):
    cfg = Config(dict(doc={'description': "mydescr", 'fmt': 'rst', 'keywords': []}))
    assert cfg['doc']['description'] == "mydescr"
    assert 'doc.description' not in opt.check(cfg)


def test_config_check_description_valid(opt):
    cfg = Config(dict(doc={'description': "", 'fmt': 'rst', 'keywords': []}))
    assert 'doc.description' in opt.check(cfg)


def test_config_check_keywords_exists(opt):
    cfg = Config(dict(doc={'description': "mydescr", 'fmt': 'rst', 'keywords': []}))
    assert len(cfg['doc']['keywords']) == 0
    assert 'doc.keywords' not in opt.check(cfg)


def test_config_check_fmt_valid(opt):
    cfg = Config(dict(doc={'description': "mydescr", 'fmt': 'walou', 'keywords': []}))
    assert 'doc.fmt' in opt.check(cfg)


def test_require(opt):
    cfg = Config(dict(base={}, doc={'fmt': 'rst'}))

    assert len(opt.require('option', cfg)) == 1
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 0
    assert len(opt.require('dvlpt', cfg)) == 0

    cfg = Config(dict(base={}, doc={'fmt': 'md'}))
    assert len(opt.require('dvlpt', cfg)) == 1
