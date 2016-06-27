from nose.tools import assert_raises

from pkglts.config_management import create_env
from pkglts.manage import default_cfg
from pkglts.manage_tools import update_opt


print(__file__)


def test_non_existing_option_raises_warning():
    env = create_env({})
    assert_raises(KeyError, lambda: update_opt('toto', env))


def test_option_fetch_parameter_list_from_config():
    env = create_env(default_cfg)
    env = update_opt('base', env)
    assert 'base' in env.globals
    cfg = env.globals['base']
    assert hasattr(cfg, 'pkgname')
    assert hasattr(cfg, 'authors')


def test_option_handle_no_parameter_list_in_config():
    env = create_env(default_cfg)
    env.globals['base'] = None
    env = update_opt('test', env)
    assert 'test' in env.globals
    assert len(tuple(env.globals['test'].items())) == 0


def test_option_use_default_from_config():
    env = create_env(default_cfg)
    env = update_opt('base', env)
    assert 'base' in env.globals
    cfg = env.globals['base']
    assert cfg.authors[0][0] == 'moi'


def test_option_already_defined_params_override_default_in_config():
    env = create_env(default_cfg)
    env = update_opt('base', env)
    cfg = env.globals['base']
    cfg.authors[0] = ("custom", "custom@email.com")

    env = update_opt('base', env)
    assert 'base' in env.globals
    assert env.globals['base'].authors[0][0] == "custom"


# def test_option_prompt_user_if_global_config_ask_for_it():
#     pkg_cfg = dict(_pkglts={'use_prompts': True})
#
#     with mock.patch('pkglts.option_tools.loc_input', return_value=''):
#         pkg_cfg = update_opt('base', pkg_cfg)
#         assert 'base' in pkg_cfg
#         cfg = pkg_cfg['base']
#         assert cfg['owner'] == 'moi'


# def test_option_pass_environment_to_config():
#     pkg_cfg = dict(_pkglts={'use_prompts': True})
#     pkg_cfg = update_opt('base', pkg_cfg, extra={'pkg_fullname': 'toto',
#                                                  'owner': 'owner'})
#     assert 'base' in pkg_cfg


# def test_option_register():
#     pkg_cfg = update_opt('base', {}, extra={'pkg_fullname': 'toto',
#                                             'owner': 'owner'})
#     pkg_cfg = update_opt('test', pkg_cfg)
#     assert 'base' in pkg_cfg
#     assert 'test' in pkg_cfg
#
#
# def test_option_look_for_dependencies():
#     extra = {"install_option_dependencies": True,
#              "pkg_fullname": 'toto',
#              'owner': 'moi'}
#     pkg_cfg = update_opt('test', {}, extra=extra)
#     assert 'base' in pkg_cfg
#     assert 'test' in pkg_cfg
