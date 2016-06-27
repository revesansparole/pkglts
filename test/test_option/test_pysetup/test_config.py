from pkglts.config_management import create_env
from pkglts.option.pysetup.config import check, parameters


def test_parameters():
    assert len(parameters) == 1


def test_config_check_intended_version_exists():
    env = create_env(dict(pysetup={'intended_versions': []}))
    assert 'intended_versions' in check(env)
