from nose.tools import with_setup
from os import listdir

from pkglts.manage import install_example_files

from .small_tools import ensure_created, rmdir


tmp_dir = "tmp_cfgex"


def setup_func():
    ensure_created(tmp_dir)


def teardown_func():
    rmdir(tmp_dir)


@with_setup(setup_func, teardown_func)
def test_install_example_returns_false_if_option_not_already_installed():
    ans = install_example_files('option', {}, tmp_dir)
    assert not ans


@with_setup(setup_func, teardown_func)
def test_install_example_ok_if_option_do_not_provide_examples():
    ans = install_example_files('base', dict(base={}), tmp_dir)
    assert not ans


@with_setup(setup_func, teardown_func)
def test_install_example_copy_files():
    assert len(listdir(tmp_dir)) == 0
    install_example_files('test', dict(test={}), tmp_dir)
    assert len(listdir(tmp_dir)) > 0


@with_setup(setup_func, teardown_func)
def test_install_example_do_not_complain_if_file_already_exists():
    install_example_files('test', dict(test={}), tmp_dir)
    install_example_files('test', dict(test={}), tmp_dir)
    assert True


# def test_config_check_tempering_of_files():
#     count = [0]
#
#     def temper(*args):
#         count[0] += 1
#
#     def temper_nothing(*args):
#         pass
#
#     pkg_cfg = dict(base=dict(pkg_fullname='toto',
#                              pkgname='toto',
#                              namespace=None))
#     with mock.patch("pkglts.option.example.config.check_tempering",
#                     new=temper):
#         with mock.patch("pkglts.option.example.config.regenerate_dir",
#                         new=temper_nothing):
#             main(pkg_cfg, dict(option_name='base'))
#
#     assert count[0] == 1
#
#
# def test_config_copy_files():
#     count = [0]
#
#     def temper(*args):
#         count[0] += 1
#
#     def temper_nothing(*args):
#         pass
#
#     pkg_cfg = dict(base=dict(pkg_fullname='toto',
#                              pkgname='toto',
#                              namespace=None),
#                    hash={})
#     with mock.patch("pkglts.option.example.config.regenerate_dir",
#                     new=temper):
#         with mock.patch("pkglts.option.example.config.check_tempering",
#                         new=temper_nothing):
#             main(pkg_cfg, dict(option_name='base'))
#
#     assert count[0] == 1
#
#
# @with_setup(setup_func, teardown_func)
# def test_config_ask_to_overwrite_files():
#     pkg_cfg = dict(base=dict(pkg_fullname='toto',
#                              pkgname='toto',
#                              namespace=None),
#                    hash={})
#
#     # create files
#     main(pkg_cfg, dict(option_name='base'))
#     cr_date = stat("src/toto/__init__.py").st_mtime
#     sleep(0.1)
#
#     # do not overwrite
#     with mock.patch('pkglts.option_tools.loc_input', return_value='n'):
#         main(pkg_cfg, dict(option_name='base'))
#         assert stat("src/toto/__init__.py").st_mtime == cr_date
#
#     # overwrite
#     with mock.patch('pkglts.option_tools.loc_input', return_value='y'):
#         main(pkg_cfg, dict(option_name='base'))
#         assert stat("src/toto/__init__.py").st_mtime > cr_date
