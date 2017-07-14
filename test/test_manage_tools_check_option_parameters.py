from pkglts.config_management import Config, default_cfg
from pkglts.manage_tools import check_option_parameters


def test_check_handle_option_config_not_existing():
    cfg = Config(default_cfg)
    assert len(check_option_parameters("toto", cfg)) == 0


def test_check_handle_option_defines_no_check():
    cfg = Config(default_cfg)
    assert len(check_option_parameters("data", cfg)) == 0
