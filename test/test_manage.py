import pytest

from pkglts.config_management import create_env, default_cfg
from pkglts.manage import add_option


def test_manage_add_opt_raise_error_if_already_installed():
    env = create_env(default_cfg)
    env = add_option("base", env)
    with pytest.raises(UserWarning):
        add_option('base', env)
