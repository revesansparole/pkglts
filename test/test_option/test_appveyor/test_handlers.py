from pkglts.config_management import Config


def test_badge():
    cfg = Config(dict(appveyor={"token": "ae34f"}, doc={"fmt": "rst"}, github={"owner": "moi", "project": "project"}))
    cfg.load_extra()
    assert "appveyor" in cfg._env.globals["appveyor"].badge.name
