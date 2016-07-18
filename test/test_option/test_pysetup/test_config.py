from pkglts.config_management import create_env
from pkglts.option.pysetup.config import check, parameters


def test_parameters():
    assert len(parameters) == 2


def test_config_check_intended_version_exists():
    env = create_env(dict(pysetup={'intended_versions': [], 'require': []}))
    assert 'intended_versions' in check(env)
    assert 'require' not in check(env)

    env = create_env(dict(pysetup={'intended_versions': ["27"],
                                   'require': [('walou', 'numpy')]}))
    assert 'require' in check(env)
