from pkglts.config_management import create_env
from pkglts.option.test.config import check, parameters


def test_parameters():
    assert len(parameters) == 1


def test_config_check_suite_names():
    for name in ('walou', ' nose'):
        env = create_env(dict(test={'suite_name': name}))
        assert 'suite_name' in check(env)
