from os.path import join as pj
from random import random

import pytest
from pkglts.config_management import Config, DEFAULT_CFG
from pkglts.hash_management import pth_as_key
from pkglts.manage_tools import find_templates, render_template
from pkglts.small_tools import ensure_created, ensure_path, rmdir


@pytest.fixture()
def tmp_dir():
    pth = "takapouet"

    ensure_created(pth)
    ensure_created(pj(pth, "src"))
    ensure_created(pj(pth, "tgt"))

    yield pth

    rmdir(pth)


def test_find_templates_walk_all_files_in_src_dir(tmp_dir):
    ensure_created(pj(tmp_dir, "src", "sub"))
    fnames = ('toto.txt', 'titi.txt', 'sub/toto.txt')
    for fname in fnames:
        pth = pj(tmp_dir, "src", fname)
        with open(pth, 'w') as f:
            f.write("lorem ipsum")

    cfg = Config(DEFAULT_CFG)
    rg_tree = {}
    find_templates(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, rg_tree)

    for fname in fnames:
        assert pth_as_key(pj(tmp_dir, 'tgt', fname)) in rg_tree


def test_find_templates_renders_path_names(tmp_dir):
    ensure_created(pj(tmp_dir, "src", "{{ custom_name }}"))
    fnames = ('{{ custom_name }}.txt', 'titi.txt',
              '{{ custom_name }}/{{ custom_name }}.txt')
    for fname in fnames:
        pth = pj(tmp_dir, "src", fname)
        with open(pth, 'w') as f:
            f.write("lorem ipsum")

    cfg = Config(DEFAULT_CFG)
    cfg._env.globals['custom_name'] = 'toto'
    rg_tree = {}
    find_templates(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, rg_tree)

    fnames = ('toto.txt', 'titi.txt', 'toto/toto.txt')
    for fname in fnames:
        assert pth_as_key(pj(tmp_dir, 'tgt', fname)) in rg_tree


def test_find_templates_handles_src_directory_no_namespace(tmp_dir):
    pth = pj(tmp_dir, "src", "src", "{{ base.pkgname }}", "test.txt")
    ensure_path(pth)
    with open(pth, 'w') as f:
        f.write("lorem ipsum")

    pkg_cfg = dict(DEFAULT_CFG)
    pkg_cfg['base'] = dict(pkgname='toto', namespace=None)
    cfg = Config(pkg_cfg)
    rg_tree = {}
    find_templates(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, rg_tree)

    tgt = pj(tmp_dir, "tgt", "src", "toto", "test.txt")
    assert pth_as_key(tgt) in rg_tree


def test_fin_templates_handles_src_directory_with_namespace(tmp_dir):
    pth = pj(tmp_dir, "src", "src", "{{ base.pkgname }}", "test.txt")
    ensure_path(pth)
    with open(pth, 'w') as f:
        f.write("lorem ipsum")

    pkg_cfg = dict(DEFAULT_CFG)
    pkg_cfg['base'] = dict(pkgname='toto', namespace='myns', namespace_method='pkg_utils')
    cfg = Config(pkg_cfg)
    rg_tree = {}
    find_templates(pj(tmp_dir, 'src'), pj(tmp_dir, 'tgt'), cfg, rg_tree)

    tgt_dir = pj(tmp_dir, "tgt")
    assert pth_as_key(tgt_dir + "/src/myns/__init__.py") in rg_tree
    assert pth_as_key(tgt_dir + "/src/myns/toto/test.txt") in rg_tree


def test_render_template_renders_file_content(tmp_dir):
    src_pth = pj(tmp_dir, "src", "test.txt")
    tgt_pth = pj(tmp_dir, "tgt", "test.txt")
    with open(src_pth, 'w') as f:
        f.write("{{ 'lorem ipsum'|upper }}")

    cfg = Config(DEFAULT_CFG)
    render_template([src_pth], tgt_pth, cfg, {})

    with open(tgt_pth, 'r') as f:
        cnt = f.read()
        assert cnt == 'LOREM IPSUM'


def test_render_template_overwrites_unprotected_files(tmp_dir):
    src_pth = pj(tmp_dir, "src", "test.txt")
    tgt_pth = pj(tmp_dir, "tgt", "test.txt")
    with open(src_pth, 'w') as f:
        f.write("{# pkglts, b0\n{{ random() }}\n#}\n")

    cfg = Config(DEFAULT_CFG)
    cfg._env.globals['random'] = random
    render_template([src_pth], tgt_pth, cfg, {})

    with open(tgt_pth, 'r') as f:
        cnt0 = f.read()

    render_template([src_pth], tgt_pth, cfg, {})

    with open(tgt_pth, 'r') as f:
        cnt1 = f.read()

    assert cnt0 != cnt1


def test_render_template_does_not_overwrite_protected_files(tmp_dir):
    src_pth = pj(tmp_dir, "src", "test.txt")
    tgt_pth = pj(tmp_dir, "tgt", "test.txt")
    with open(src_pth, 'w') as f:
        f.write("{# pkglts, b0\n{{ random() }}\n#}\n")

    cfg = Config(DEFAULT_CFG)
    cfg._env.globals['random'] = random
    render_template([src_pth], tgt_pth, cfg, {})

    with open(tgt_pth, 'r') as f:
        cnt0 = f.read()

    overwrite = {pth_as_key(tgt_pth): False}
    render_template([src_pth], tgt_pth, cfg, overwrite)

    with open(tgt_pth, 'r') as f:
        cnt1 = f.read()

    assert cnt0 == cnt1


def test_render_template_does_not_overwrite_outside_protected_blocks(tmp_dir):
    src_pth = pj(tmp_dir, "src", "test.txt")
    tgt_pth = pj(tmp_dir, "tgt", "test.txt")
    with open(src_pth, 'w') as f:
        f.write("{# pkglts, b0\nLOREM IPSUM\n#}\n")

    with open(tgt_pth, 'w') as f:
        f.write("Toto start\n{# pkglts, b0\nWTF?\n#}\nToto end\n")

    cfg = Config(DEFAULT_CFG)
    render_template([src_pth], tgt_pth, cfg, {})

    with open(tgt_pth, 'r') as f:
        cnt = f.read()

    assert cnt == "Toto start\n{# pkglts, b0\nLOREM IPSUM\n#}\nToto end\n"
