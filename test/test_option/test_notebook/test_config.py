from pathlib import Path

import pytest
from pkglts.config_management import Config
from pkglts.option.notebook.option import OptionNotebook
from pkglts.small_tools import ensure_created, rmdir


@pytest.fixture()
def opt():
    return OptionNotebook("notebook")


@pytest.fixture()
def cfg():
    return Config()


@pytest.fixture()
def tmp_dir():
    pth = Path("nb_test_config")
    ensure_created(pth)

    yield pth

    rmdir(pth)


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg["notebook"]) == 1


def test_config_check_src_directory(opt, cfg, tmp_dir):
    cfg["notebook"] = {"src_directory": "failed_nb"}
    assert "notebook.src_directory" in opt.check(cfg)

    cfg["notebook"] = {"src_directory": tmp_dir}
    assert "notebook.src_directory" not in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
