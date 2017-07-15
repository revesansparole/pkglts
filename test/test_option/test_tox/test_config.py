from pkglts.config_management import Config
from pkglts.option.tox.config import require


def test_require():
    cfg = Config(dict(base={}, tox={}))

    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 1
