import pytest
from pkglts.config_management import Config
from pkglts.option.sphinx.option import OptionSphinx


@pytest.fixture()
def opt():
    return OptionSphinx('sphinx')


def test_version_is_defined(opt):
    assert opt.version() != "0.0.0"


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['sphinx']) == 4


def test_config_checks_doc_fmt(opt):
    cfg = Config(dict(doc={'fmt': 'md'}))
    opt.update_parameters(cfg)
    assert 'doc.fmt' in opt.check(cfg)


def test_config_check_sphinx_theme(opt):
    cfg = Config(dict(doc={'fmt': 'rst'}))
    opt.update_parameters(cfg)

    for theme in (1, None,):
        cfg['sphinx']['theme'] = theme
        assert 'sphinx.theme' in opt.check(cfg)


def test_config_check_sphinx_gallery(opt):
    cfg = Config(dict(doc={'fmt': 'rst'}))
    opt.update_parameters(cfg)

    assert 'sphinx.gallery' not in opt.check(cfg)

    for pth in ("a" * 256, "toto/:titi/"):
        cfg['sphinx']['gallery'] = pth
        assert 'sphinx.gallery' in opt.check(cfg)


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 1
