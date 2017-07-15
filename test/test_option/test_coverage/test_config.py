from pkglts.config_management import Config
from pkglts.option.coverage.config import require


def test_require():
    cfg = Config(dict(coverage={}, test={'suite_name': 'pytest'}))

    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 2

    cfg = Config(dict(coverage={}, test={'suite_name': 'nose'}))
    assert len(require('dvlpt', cfg)) == 1
