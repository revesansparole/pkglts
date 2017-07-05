from pkglts.config_management import create_env
from pkglts.option.data.config import require


def test_require():
    cfg = dict(base={}, data={})
    env = create_env(cfg)

    assert len(require('option', env)) == 1
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 0
