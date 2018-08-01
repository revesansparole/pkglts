import pytest
from pkglts.config_management import Config
from pkglts.option.sphinx.option import OptionSphinx


@pytest.fixture()
def opt():
    return OptionSphinx('sphinx')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['sphinx']) == 3


def test_config_checks_doc_fmt(opt):
    cfg = Config(dict(doc={'fmt': 'md'}, sphinx={'theme': "default"}))
    assert 'doc.fmt' in opt.check(cfg)


def test_config_check_sphinx_theme(opt):
    for theme in (1, None,):
        cfg = Config(dict(doc={'fmt': 'rst'}, sphinx={'theme': theme}))
        assert 'sphinx.theme' in opt.check(cfg)


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 3


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 1
