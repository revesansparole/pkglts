from pkglts.config_management import Config
from pkglts.option.landscape.config import require


def test_require():
    cfg = Config(dict(landscape={}))

    assert len(require('option', cfg)) == 2
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
