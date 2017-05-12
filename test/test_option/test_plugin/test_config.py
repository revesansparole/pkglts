from pkglts.config_management import create_env
from pkglts.option.plugin.config import check, parameters


def test_parameters():
    assert len(parameters) == 0


def test_config_check_sphinx_theme():
        env = create_env(dict(plugin={'tugudu': 'poutou'}))
        assert len(check(env)) == 0
