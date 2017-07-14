from pkglts.config_management import Config
from pkglts.option.sphinx.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 2


def test_config_check_sphinx_theme():
    for theme in (1, None,):
        cfg = Config(dict(sphinx={'theme': theme}))
        assert 'theme' in check(cfg)


def test_require():
    cfg = Config(dict(sphinx={}))

    assert len(require('option', cfg)) == 2
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 1
