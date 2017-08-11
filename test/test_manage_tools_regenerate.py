from os.path import join as pj
from os.path import exists
import pytest
from random import random

from pkglts.config_management import Config, default_cfg
from pkglts.hash_management import pth_as_key
from pkglts.manage_tools import regenerate_dir

from .small_tools import ensure_created, ensure_path, rmdir


@pytest.fixture()
def tmp_dir():
    pth = "takapouet"

    ensure_created(pth)
    ensure_created(pj(pth, "src"))
    ensure_created(pj(pth, "tgt"))

    yield pth

    rmdir(pth)


def test_regenerate_dir_walk_all_files_in_src_dir(tmp_dir):
    ensure_created(pj(tmp_dir, "src", "sub"))
    fnames = ('toto.txt', 'titi.txt', 'sub/toto.txt')
    for fname in fnames:
        pth = pj(tmp_dir, "src", fname)
        with open(pth, 'w') as f:
            f.write("lorem ipsum")

    cfg = Config(default_cfg)
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, {})

    for fname in fnames:
        assert exists(pj(tmp_dir, 'tgt', fname))


def test_regenerate_dir_render_file_content(tmp_dir):
    pth = pj(tmp_dir, "src", "test.txt")
    with open(pth, 'w') as f:
        f.write("{{ 'lorem ipsum'|upper }}")

    cfg = Config(default_cfg)
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, {})

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'r') as f:
        cnt = f.read()
        assert cnt == 'LOREM IPSUM'


def test_regenerate_dir_render_path_names(tmp_dir):
    ensure_created(pj(tmp_dir, "src", "{{ custom_name }}"))
    fnames = ('{{ custom_name }}.txt', 'titi.txt',
              '{{ custom_name }}/{{ custom_name }}.txt')
    for fname in fnames:
        pth = pj(tmp_dir, "src", fname)
        with open(pth, 'w') as f:
            f.write("lorem ipsum")

    cfg = Config(default_cfg)
    cfg._env.globals['custom_name'] = 'toto'
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, {})

    fnames = ('toto.txt', 'titi.txt', 'toto/toto.txt')
    for fname in fnames:
        assert exists(pj(tmp_dir, 'tgt', fname))


def test_regenerate_handle_src_directory_no_namespace(tmp_dir):
    pth = pj(tmp_dir, "src", "src", "{{ base.pkgname }}", "test.txt")
    ensure_path(pth)
    with open(pth, 'w') as f:
        f.write("lorem ipsum")

    pkg_cfg = dict(default_cfg)
    pkg_cfg['base'] = dict(pkgname='toto', namespace=None)
    cfg = Config(pkg_cfg)
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, {})

    tgt = pj(tmp_dir, "tgt", "src", "toto", "test.txt")
    assert exists(tgt)


def test_regenerate_handle_src_directory_with_namespace(tmp_dir):
    pth = pj(tmp_dir, "src", "src", "{{ base.pkgname }}", "test.txt")
    ensure_path(pth)
    with open(pth, 'w') as f:
        f.write("lorem ipsum")

    pkg_cfg = dict(default_cfg)
    pkg_cfg['base'] = dict(pkgname='toto', namespace='myns', namespace_method='pkg_utils')
    cfg = Config(pkg_cfg)
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, {})

    tgt_dir = pj(tmp_dir, "tgt")
    assert exists(tgt_dir + "/src")
    assert exists(tgt_dir + "/src/myns")
    assert exists(tgt_dir + "/src/myns/__init__.py")
    assert exists(tgt_dir + "/src/myns/toto")
    assert exists(tgt_dir + "/src/myns/toto/test.txt")


def test_regenerate_do_overwrite_unprotected_files(tmp_dir):
    pth = pj(tmp_dir, "src", "test.txt")
    with open(pth, 'w') as f:
        f.write("{# pkglts, b0\n{{ random() }}\n#}\n")

    cfg = Config(default_cfg)
    cfg._env.globals['random'] = random
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, {})

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'r') as f:
        cnt0 = f.read()

    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, {})

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'r') as f:
        cnt1 = f.read()

    assert cnt0 != cnt1


def test_regenerate_do_not_overwrite_protected_files(tmp_dir):
    pth = pj(tmp_dir, "src", "test.txt")
    with open(pth, 'w') as f:
        f.write("{# pkglts, b0\n{{ random() }}\n#}\n")

    cfg = Config(default_cfg)
    cfg._env.globals['random'] = random
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, {})

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'r') as f:
        cnt0 = f.read()

    overwrite = {pth_as_key(pth): False}
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, overwrite)

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'r') as f:
        cnt1 = f.read()

    assert cnt0 == cnt1


def test_regenerate_do_not_overwrite_outside_protected_blocks(tmp_dir):
    pth = pj(tmp_dir, "src", "test.txt")
    with open(pth, 'w') as f:
        f.write("{# pkglts, b0\nLOREM IPSUM\n#}\n")

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'w') as f:
        f.write("Toto start\n{# pkglts, b0\nWTF?\n#}\nToto end\n")

    cfg = Config(default_cfg)
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, {})

    with open(pth, 'r') as f:
        cnt = f.read()

    assert cnt == "Toto start\n{# pkglts, b0\nLOREM IPSUM\n#}\nToto end\n"

