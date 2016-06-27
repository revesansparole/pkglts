from pkglts.config_management import create_env
from pkglts.option.pypi.config import check, parameters


def test_parameters():
    assert len(parameters) == 1


def test_config_check_classifiers_exists():
    env = create_env(dict(pypi={'classifiers': []}))
    assert 'classifiers' in check(env)
