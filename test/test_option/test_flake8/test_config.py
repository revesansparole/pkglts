from pkglts.config_management import Config
from pkglts.option.flake8.config import require


def test_require():
    cfg = Config(dict(base={}, flake8={}))

    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 1
