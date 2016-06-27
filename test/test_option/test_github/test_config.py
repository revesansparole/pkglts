from pkglts.config_managment import create_env
from pkglts.option.github.config import check, parameters


def test_parameters():
    assert len(parameters) == 3


def test_config_check_project_exists():
    env = create_env(dict(github={'owner': "", 'project': "", "url": ""}))
    assert 'project' in check(env)
