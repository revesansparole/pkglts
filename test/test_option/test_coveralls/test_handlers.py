from pkglts.config_management import Config


def test_badge():
    cfg = Config(dict(coveralls={},
                      github={'owner': "moi", 'project': "project"}))
    cfg.load_extra()
    assert ".. image:" in cfg._env.globals['coveralls'].badge
