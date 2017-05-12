from pkglts.config_management import create_env
from pkglts.option.sphinx.config import check, parameters


def test_parameters():
    assert len(parameters) == 2


def test_config_check_sphinx_theme():
    for theme in (1, None,):
        env = create_env(dict(sphinx={'theme': theme}))
        assert 'theme' in check(env)
