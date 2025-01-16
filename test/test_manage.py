import pytest

from pkglts.config_management import Config, DEFAULT_CFG
from pkglts.manage import add_option


def test_manage_add_opt_raise_error_if_already_installed():
    cfg = Config(DEFAULT_CFG)
    cfg = add_option("base", cfg)
    with pytest.raises(UserWarning):
        add_option("base", cfg)
