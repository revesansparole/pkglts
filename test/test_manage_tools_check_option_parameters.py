from pkglts.config_management import create_env
from pkglts.manage import default_cfg
from pkglts.manage_tools import check_option_parameters


def test_check_handle_option_config_not_existing():
    env = create_env(default_cfg)
    assert len(check_option_parameters("toto", env)) == 0


def test_check_handle_option_defines_no_check():
    env = create_env(default_cfg)
    assert len(check_option_parameters("test", env)) == 0
