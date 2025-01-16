from pkglts.config_management import Config


def test_badge():
    cfg = Config(dict(lgtm={}, doc={"fmt": "rst"}, github={"owner": "moi", "project": "project"}))
    cfg.load_extra()
    assert "lgtm" in cfg._env.globals["lgtm"].badge.name
