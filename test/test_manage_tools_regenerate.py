from nose.tools import with_setup
from os.path import join as pj
from os.path import exists
from random import random

from pkglts.config_management import create_env, default_cfg
from pkglts.hash_management import pth_as_key
from pkglts.manage_tools import regenerate_dir

from .small_tools import ensure_created, ensure_path, rmdir


tmp_dir = "takapouet"


def setup():
    ensure_created(tmp_dir)
    ensure_created(pj(tmp_dir, "src"))
    ensure_created(pj(tmp_dir, "tgt"))


def teardown():
    rmdir(tmp_dir)


@with_setup(setup, teardown)
def test_regenerate_dir_walk_all_files_in_src_dir():
    ensure_created(pj(tmp_dir, "src", "sub"))
    fnames = ('toto.txt', 'titi.txt', 'sub/toto.txt')
    for fname in fnames:
        pth = pj(tmp_dir, "src", fname)
        with open(pth, 'w') as f:
            f.write("lorem ipsum")

    env = create_env(default_cfg)
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), env, {})

    for fname in fnames:
        assert exists(pj(tmp_dir, 'tgt', fname))


@with_setup(setup, teardown)
def test_regenerate_dir_render_file_content():
    pth = pj(tmp_dir, "src", "test.txt")
    with open(pth, 'w') as f:
        f.write("{{ 'lorem ipsum'|upper }}")

    env = create_env(default_cfg)
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), env, {})

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'r') as f:
        cnt = f.read()
        assert cnt == 'LOREM IPSUM'


@with_setup(setup, teardown)
def test_regenerate_dir_render_path_names():
    ensure_created(pj(tmp_dir, "src", "{{ custom_name }}"))
    fnames = ('{{ custom_name }}.txt', 'titi.txt',
              '{{ custom_name }}/{{ custom_name }}.txt')
    for fname in fnames:
        pth = pj(tmp_dir, "src", fname)
        with open(pth, 'w') as f:
            f.write("lorem ipsum")

    env = create_env(default_cfg)
    env.globals['custom_name'] = 'toto'
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), env, {})

    fnames = ('toto.txt', 'titi.txt', 'toto/toto.txt')
    for fname in fnames:
        assert exists(pj(tmp_dir, 'tgt', fname))


@with_setup(setup, teardown)
def test_regenerate_handle_src_directory_no_namespace():
    pth = pj(tmp_dir, "src", "src", "{{ base.pkgname }}", "test.txt")
    ensure_path(pth)
    with open(pth, 'w') as f:
        f.write("lorem ipsum")

    cfg = dict(default_cfg)
    cfg['base'] = dict(pkgname='toto', namespace=None)
    env = create_env(cfg)
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), env, {})

    tgt = pj(tmp_dir, "tgt", "src", "toto", "test.txt")
    assert exists(tgt)


@with_setup(setup, teardown)
def test_regenerate_handle_src_directory_with_namespace():
    pth = pj(tmp_dir, "src", "src", "{{ base.pkgname }}", "test.txt")
    ensure_path(pth)
    with open(pth, 'w') as f:
        f.write("lorem ipsum")

    cfg = dict(default_cfg)
    cfg['base'] = dict(pkgname='toto', namespace='myns', namespace_method='pkg_utils')
    env = create_env(cfg)
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), env, {})

    tgt_dir = pj(tmp_dir, "tgt")
    assert exists(tgt_dir + "/src")
    assert exists(tgt_dir + "/src/myns")
    assert exists(tgt_dir + "/src/myns/__init__.py")
    assert exists(tgt_dir + "/src/myns/toto")
    assert exists(tgt_dir + "/src/myns/toto/test.txt")


@with_setup(setup, teardown)
def test_regenerate_do_overwrite_unprotected_files():
    pth = pj(tmp_dir, "src", "test.txt")
    with open(pth, 'w') as f:
        f.write("{# pkglts, b0\n{{ random() }}\n#}")

    env = create_env(default_cfg)
    env.globals['random'] = random
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), env, {})

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'r') as f:
        cnt0 = f.read()

    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), env, {})

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'r') as f:
        cnt1 = f.read()

    assert cnt0 != cnt1


@with_setup(setup, teardown)
def test_regenerate_do_not_overwrite_protected_files():
    pth = pj(tmp_dir, "src", "test.txt")
    with open(pth, 'w') as f:
        f.write("{# pkglts, b0\n{{ random() }}\n#}")

    env = create_env(default_cfg)
    env.globals['random'] = random
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), env, {})

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'r') as f:
        cnt0 = f.read()

    overwrite = {pth_as_key(pth): False}
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), env, overwrite)

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'r') as f:
        cnt1 = f.read()

    assert cnt0 == cnt1


@with_setup(setup, teardown)
def test_regenerate_do_not_overwrite_outside_protected_blocks():
    pth = pj(tmp_dir, "src", "test.txt")
    with open(pth, 'w') as f:
        f.write("{# pkglts, b0\nLOREM IPSUM\n#}")

    pth = pj(tmp_dir, "tgt", "test.txt")
    with open(pth, 'w') as f:
        f.write("Toto start\n{# pkglts, b0\nWTF?\n#}\nToto end\n")

    env = create_env(default_cfg)
    regenerate_dir(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), env, {})

    with open(pth, 'r') as f:
        cnt = f.read()

    assert cnt == "Toto start\n{# pkglts, b0\nLOREM IPSUM\n#}\nToto end\n"

