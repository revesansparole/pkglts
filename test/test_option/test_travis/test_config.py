from pkglts.config_management import Config
from pkglts.option.travis.config import require


def test_require():
    cfg = Config(dict(base={}, travis={}))

    assert len(require('option', cfg)) == 2
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
