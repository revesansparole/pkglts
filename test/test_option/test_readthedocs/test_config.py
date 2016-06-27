from pkglts.config_management import create_env
from pkglts.option.readthedocs.config import check, parameters


def test_parameters():
    assert len(parameters) == 1


def test_config_check_project_exists():
    env = create_env(dict(readthedocs={'project': ""}))
    assert 'project' in check(env)
