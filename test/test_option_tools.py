import pytest

from pkglts.option_tools import get_user_permission


loc_input = 'pkglts.option_tools.loc_input'


def test_user_permission(mocker):
    with mocker.patch(loc_input, return_value=''):
        assert get_user_permission('action')

    with mocker.patch(loc_input, return_value='y'):
        assert get_user_permission('action')

    with mocker.patch(loc_input, return_value='n'):
        assert not get_user_permission('action')

    with mocker.patch(loc_input, return_value='N'):
        assert not get_user_permission('action')


# def test_get_key():
#     assert get_key('toto', {'toto': 'titi'}) == 'titi'
#
#
# def test_get_key_nested():
#     assert get_key('toto.titi', {'toto': {'titi': 'tata'}}) == 'tata'
#
#
# def test_get_key_returns_none_for_unknown_key():
#     assert get_key('tata', {'toto': {'titi': 'tata'}}) is None
#     assert get_key('toto.tata', {'toto': {'titi': 'tata'}}) is None
#     assert get_key('titi', {'toto': {'titi': 'tata'}}) is None
#
#
# def test_ask_arg_do_not_prompt_user_if_value_in_extra(mocker):
#     with mocker.patch(loc_input, return_value='useless'):
#         assert ask_arg('toto', None, None, {'toto': 1}) == 1
#
#
# def test_ask_arg_find_default_in_pkg_cfg(mocker):
#     with mocker.patch(loc_input, return_value=''):
#         assert ask_arg('toto', {'toto': 1}) == '1'
#         assert ask_arg('toto', {'titi': 1}) == ''
#         assert ask_arg('toto') == ''
#
#
# def test_ask_use_default_if_everything_fail_only(mocker):
#     with mocker.patch(loc_input, return_value=''):
#         assert ask_arg('toto', {'toto': 1}, 2) == '1'
#         assert ask_arg('toto', {'titi': 1}, 2) == '2'
#
#
# def test_ask_arg_user_bypass_default(mocker):
#     with mocker.patch(loc_input, return_value='myvalue'):
#         assert ask_arg('toto', {'toto': 1}, 0, {}) == 'myvalue'
#         assert ask_arg('toto', {}, 0, {}) == 'myvalue'
#         assert ask_arg('toto') == 'myvalue'
#
#
# def test_ask_arg_handle_list(mocker):
#     with mocker.patch(loc_input, return_value=''):
#         res = ask_arg('keys', {}, ["1"], {})
#         assert res == ["1"]
#         res = ask_arg('keys', {}, ["1", "2"], {})
#         assert res == ["1", "2"]
#         res = ask_arg('keys', {'keys': ["1", "2"]}, [], {})
#         assert res == ["1", "2"]
#         res = ask_arg('keys', {'keys': ["1", "2"]}, ["1"], {})
#         assert res == ["1", "2"]
#         res = ask_arg('keys', {'keys': ["1"]}, ["1", "2"], {})
#         assert res == ["1"]
#         assert_raises(UserWarning, lambda: ask_arg('keys', {'keys': "1"},
#                                                    ["1", "2"], {}))
