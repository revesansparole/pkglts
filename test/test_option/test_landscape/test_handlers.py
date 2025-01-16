from pkglts.config_management import Config


def test_badge():
    cfg = Config(dict(landscape={}, doc={"fmt": "rst"}, github={"owner": "moi", "project": "project"}))
    cfg.load_extra()
    assert "landscape" in cfg._env.globals["landscape"].badge.name
