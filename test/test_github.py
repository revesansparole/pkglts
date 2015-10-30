import json
import mock
from nose.tools import assert_raises, with_setup
from os import chdir, getcwd, mkdir
from os.path import exists
from shutil import rmtree

from pkglts.github import ensure_login


print(__file__)

tmp_dir = 'github_tmp'


def setup():
    if not exists(tmp_dir):
        mkdir(tmp_dir)


def teardown():
    if exists(tmp_dir):
        rmtree(tmp_dir)


@with_setup(setup, teardown)
def test_github_login_raise_error_if_github_not_option():
    assert_raises(KeyError, lambda: ensure_login({}))


@with_setup(setup, teardown)
def test_github_login_do_not_prompt_user_if_already_done():
    cfg = dict(github={})
    cfg['_session'] = {}
    cfg['_session']['github'] = "gh"
    cfg['_session']['github_repo'] = "repo"

    with mock.patch("pkglts.github.ask_arg", side_effect=UserWarning):
        ensure_login(cfg)


@with_setup(setup, teardown)
def test_github_login_do_not_recurse_infinitively():
    cfg = dict(github=dict(owner="moi", project="mine"))
    with mock.patch("pkglts.github.ask_arg", return_value=""):
        assert_raises(UserWarning, lambda: ensure_login(cfg))


# @with_setup(setup, teardown)
# def test_github_login_do_not_prompt_user_if_cookie_present():
#     # TODO: arrg, remove ugly
#     cfg = dict(github=dict(owner="moi", project="mine"))
#     cwd = getcwd()
#     chdir(tmp_dir)
#     cookie = dict(login='toto', password='pwd')
#     with open(".cookie.json", 'w') as f:
#         json.dump(cookie, f)
#
#     assert_raises(UserWarning, lambda: ensure_login(cfg))
#
#     chdir(cwd)
#     # TODO: don't know how to do it without valid credentials
#     pass
