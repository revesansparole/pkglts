from os import mkdir, rmdir
from os.path import exists

import pytest
from pkglts.config_management import Config
from pkglts.option.notebook.option import OptionNotebook


@pytest.fixture()
def opt():
    return OptionNotebook('notebook')


@pytest.fixture()
def tmp_dir():
    pth = "nb_test_config"
    mkdir(pth)

    yield pth

    if exists(pth):
        rmdir(pth)


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['notebook']) == 1


def test_config_check_src_directory(opt, tmp_dir):
    cfg = Config(dict(notebook={'src_directory': "failed_nb"}))
    assert 'notebook.src_directory' in opt.check(cfg)

    cfg = Config(dict(notebook={'src_directory': tmp_dir}))
    assert 'notebook.src_directory' not in opt.check(cfg)


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(opt.require('option', cfg)) == 1
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 0
    assert len(opt.require('dvlpt', cfg)) == 1
