from pathlib import Path

import pytest
from pkglts.manage import clean
from pkglts.small_tools import ensure_created, rmdir


@pytest.fixture()
def tmp_dir():
    pth = Path('toto_manage_clean')
    ensure_created(pth)

    yield pth

    rmdir(pth)


def test_clean_remove_pyc_files(tmp_dir):
    pth = tmp_dir / "toto.pyc"
    pth.write_text("toto")

    clean(tmp_dir)

    assert not pth.exists()


def test_clean_remove_pycache_directories(tmp_dir):
    pycache = tmp_dir / "__pycache__"
    ensure_created(pycache)
    pth = pycache / "toto.py"
    pth.write_text("toto")

    clean(tmp_dir)

    assert not pycache.exists()
    assert not pth.exists()


def test_clean_do_not_remove_py_files(tmp_dir):
    pth = tmp_dir / "toto.py"
    pth.write_text("toto")

    clean(tmp_dir)

    assert pth.exists()


def test_clean_do_not_remove_hidden_files(tmp_dir):
    pth = tmp_dir / ".toto.pyc"
    pth.write_text("toto")

    clean(tmp_dir)

    assert pth.exists()


def test_clean_do_not_explore_hidden_directories(tmp_dir):
    hidden = tmp_dir / ".test"
    ensure_created(hidden)
    pth = hidden / "toto.py"
    pth.write_text("toto")

    clean(tmp_dir)

    assert hidden.exists()
    assert pth.exists()


def test_clean_do_not_explore_clean_no_directories(tmp_dir):
    hidden = tmp_dir / "test"
    ensure_created(hidden)
    pth = hidden / "toto.py"
    pth.write_text("toto")

    (hidden / "clean.no").touch()

    clean(tmp_dir)

    assert hidden.exists()
    assert pth.exists()


def test_clean_remove_dist_build_directories(tmp_dir):
    for name in ("dist", "build"):
        ensure_created(tmp_dir / name)

    clean(tmp_dir)

    assert len(tuple(tmp_dir.iterdir())) == 0
