from nose.tools import with_setup
from os import listdir
from os.path import exists
from os.path import join as pj

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
    install_example_files('test',
                          dict(base={'pkgname': 'toto', 'namespace': None},
                               test={}), tmp_dir)
    assert len(listdir(tmp_dir)) > 0
    assert exists(pj(tmp_dir, "src", "toto", "example.py"))
    assert exists(pj(tmp_dir, "test", "test_example.py"))


@with_setup(setup_func, teardown_func)
def test_install_example_copy_binary_files():
    assert len(listdir(tmp_dir)) == 0
    install_example_files('data',
                          dict(base={'pkgname': 'toto', 'namespace': None},
                               data={}), tmp_dir)
    assert len(listdir(tmp_dir)) > 0
    assert exists(pj(tmp_dir, "src", "toto_data", "ext_data.png"))


@with_setup(setup_func, teardown_func)
def test_install_example_do_not_complain_if_file_already_exists():
    install_example_files('test',
                          dict(base={'pkgname': 'toto', 'namespace': None},
                               test={}), tmp_dir)
    install_example_files('test',
                          dict(base={'pkgname': 'toto', 'namespace': None},
                               test={}), tmp_dir)
    assert True


@with_setup(setup_func, teardown_func)
def test_install_example_handles_namespace():
    pkg_cfg = dict(base={'pkgname': 'toto', 'namespace': 'oa'}, test={})
    install_example_files('test', pkg_cfg, tmp_dir)
    assert exists(pj(tmp_dir, "test", "test_example.py"))
    assert not exists(pj(tmp_dir, "src", "toto", "example.py"))
    assert exists(pj(tmp_dir, "src", "oa", "toto", "example.py"))
