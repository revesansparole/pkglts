import pytest

from pkglts.config_management import Config, default_cfg
from pkglts.manage_tools import update_opt


print(__file__)


def test_non_existing_option_raises_warning():
    cfg = Config({})
    with pytest.raises(KeyError):
        update_opt('toto', cfg)


def test_option_fetch_parameter_list_from_config():
    cfg = Config(default_cfg)
    cfg = update_opt('base', cfg)
    assert 'base' in cfg
    assert 'pkgname' in cfg['base']
    assert 'authors' in cfg['base']


def test_option_handle_no_parameter_list_in_config():
    cfg = Config(default_cfg)
    cfg._env.globals['base'] = None
    cfg = update_opt('data', cfg)
    assert 'data' in cfg
    assert len(tuple(cfg['data'].items())) == 1


def test_option_use_default_from_config():
    cfg = Config(default_cfg)
    cfg = update_opt('base', cfg)
    assert 'base' in cfg
    assert cfg['base']['authors'][0][0] == 'moi'


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
