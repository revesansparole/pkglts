from pkglts.config_management import create_env
from pkglts.option.coverage.config import require


def test_require():
    cfg = dict(coverage={}, test={'suite_name': 'pytest'})
    env = create_env(cfg)

    assert len(require('option', env)) == 1
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 2

    cfg = dict(coverage={}, test={'suite_name': 'nose'})
    env = create_env(cfg)
    assert len(require('dvlpt', env)) == 1
