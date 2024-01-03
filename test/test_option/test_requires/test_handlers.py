from pkglts.config_management import Config


def test_badge():
    cfg = Config(dict(requires={},
                      doc={'fmt': 'rst'},
                      github={'owner': "moi", 'project': "project"}))
    cfg.load_extra()
    assert "requires" in cfg._env.globals['requires'].badge.name
