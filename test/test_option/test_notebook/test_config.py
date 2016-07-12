from nose.tools import with_setup
from os import mkdir, rmdir
from os.path import exists

from pkglts.config_management import create_env
from pkglts.option.notebook.config import parameters, check

tmp_dir = "nb_test_config"


def test_parameters():
    assert len(parameters) == 1


def setup_func():
    mkdir(tmp_dir)


def teardown_func():
    if exists(tmp_dir):
        rmdir(tmp_dir)


@with_setup(setup=setup_func, teardown=teardown_func)
def test_config_check_src_directory():
    env = create_env(dict(notebook={'src_directory': "failed_nb"}))
    assert 'src_directory' in check(env)

    env = create_env(dict(notebook={'src_directory': tmp_dir}))
    assert 'src_directory' not in check(env)
