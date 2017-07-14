from os import mkdir, rmdir
from os.path import exists
import pytest

from pkglts.config_management import Config
from pkglts.option.notebook.config import check, require, update_parameters


@pytest.fixture()
def tmp_dir():
    pth = "nb_test_config"
    mkdir(pth)

    yield pth

    if exists(pth):
        rmdir(pth)


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['notebook']) == 1


def test_config_check_src_directory(tmp_dir):
    cfg = Config(dict(notebook={'src_directory': "failed_nb"}))
    assert 'src_directory' in check(cfg)

    cfg = Config(dict(notebook={'src_directory': tmp_dir}))
    assert 'src_directory' not in check(cfg)


def test_require():
    cfg = Config(dict(notebook={}))

    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 1
