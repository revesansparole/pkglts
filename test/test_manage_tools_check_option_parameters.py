from pkglts.manage import default_cfg
from pkglts.manage_tools import check_option_parameters


def test_check_handle_option_config_not_existing():
    pkg_cfg = dict(default_cfg)
    assert len(check_option_parameters("toto", pkg_cfg)) == 0


def test_check_handle_option_defines_no_check():
    pkg_cfg = dict(default_cfg)
    assert len(check_option_parameters("test", pkg_cfg)) == 0
