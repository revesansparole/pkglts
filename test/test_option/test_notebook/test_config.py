from os import mkdir, rmdir
from os.path import exists
import pytest

from pkglts.config_management import create_env
from pkglts.option.notebook.config import parameters, check, require


@pytest.fixture()
def tmp_dir():
    pth = "nb_test_config"
    mkdir(pth)

    yield pth

    if exists(pth):
        rmdir(pth)


def test_parameters():
    assert len(parameters) == 1


def test_config_check_src_directory(tmp_dir):
    env = create_env(dict(notebook={'src_directory': "failed_nb"}))
    assert 'src_directory' in check(env)

    env = create_env(dict(notebook={'src_directory': tmp_dir}))
    assert 'src_directory' not in check(env)


def test_require():
    cfg = dict(notebook={})
    env = create_env(cfg)

    assert len(require('option', env)) == 1
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 1
