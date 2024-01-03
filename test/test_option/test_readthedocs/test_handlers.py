from pkglts.config_management import Config


def test_badge():
    cfg = Config(dict(doc={'fmt': 'rst'}, readthedocs={'project': "project"}))
    cfg.load_extra()
    assert "readthedocs" in cfg._env.globals['readthedocs'].badge.name
