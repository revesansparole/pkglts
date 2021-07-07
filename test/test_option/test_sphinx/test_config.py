import pytest
from pkglts.config_management import Config
from pkglts.option.sphinx.option import OptionSphinx


@pytest.fixture()
def opt():
    return OptionSphinx('sphinx')


@pytest.fixture()
def cfg():
    return Config(dict(doc={'fmt': 'rst'}))


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg['sphinx']) == 5


def test_config_checks_doc_fmt(opt, cfg):
    cfg['doc'] = {'fmt': 'md'}
    opt.update_parameters(cfg)
    assert 'doc.fmt' in opt.check(cfg)


def test_config_check_sphinx_theme(opt, cfg):
    opt.update_parameters(cfg)

    for theme in (1, None,):
        cfg['sphinx']['theme'] = theme
        assert 'sphinx.theme' in opt.check(cfg)


def test_config_check_sphinx_gallery(opt, cfg):
    opt.update_parameters(cfg)

    assert 'sphinx.gallery' not in opt.check(cfg)

    for pth in ("a" * 256,):
        cfg['sphinx']['gallery'] = pth
        assert 'sphinx.gallery' in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 2


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 1
