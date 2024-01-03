from pkglts.config_management import Config


def test_badge():
    cfg = Config(dict(coveralls={},
                      doc={'fmt': 'rst'},
                      github={'owner': "moi", 'project': "project"}))
    cfg.load_extra()
    assert "coveralls" in cfg._env.globals['coveralls'].badge.name
