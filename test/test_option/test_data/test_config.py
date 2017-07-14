from pkglts.config_management import Config
from pkglts.option.data.config import require


def test_require():
    cfg = Config(dict(base={}, data={}))

    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
