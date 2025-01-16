import pytest

from pkglts.config_management import Config


def test_generate():
    cfg = Config(dict(license=dict(name="mit", year="2015", organization="org", project="project")))
    cfg.load_extra()
    assert len(cfg._env.globals["license"].full_text) > 0


def test_generate_raise_error_if_license_do_not_exists():
    cfg = dict(name="tugudu", year="2015", organization="org", project="project")
    with pytest.raises(IOError):
        Config(dict(license=cfg)).load_extra()
