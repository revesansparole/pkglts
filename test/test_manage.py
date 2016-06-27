from nose.tools import assert_raises

from pkglts.config_managment import create_env, default_cfg
from pkglts.manage import add_option


def test_manage_add_opt_raise_error_if_already_installed():
    env = create_env(default_cfg)
    env = add_option("base", env)
    assert_raises(UserWarning, lambda: add_option('base', env))
