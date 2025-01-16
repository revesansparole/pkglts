from pathlib import Path
from random import random

import pytest
from pkglts.config_management import Config, DEFAULT_CFG
from pkglts.hash_management import pth_as_key
from pkglts.manage_tools import find_templates, render_template
from pkglts.small_tools import ensure_created, ensure_path, rmdir


@pytest.fixture()
def tmp_dir():
    pth = Path("takapouet")

    ensure_created(pth)
    ensure_created(pth / "src")
    ensure_created(pth / "tgt")

    yield pth

    rmdir(pth)


def test_find_templates_walk_all_files_in_src_dir(tmp_dir):
    ensure_created(tmp_dir / "src/sub")
    fnames = ("toto.txt", "titi.txt", "sub/toto.txt")
    for fname in fnames:
        pth = tmp_dir / "src" / fname
        pth.write_text("lorem ipsum")

    cfg = Config(DEFAULT_CFG)
    rg_tree = {}
    find_templates(tmp_dir / "src", tmp_dir / "tgt", cfg, rg_tree)

    for fname in fnames:
        assert pth_as_key(tmp_dir / "tgt" / fname) in rg_tree


def test_find_templates_renders_path_names(tmp_dir):
    ensure_created(tmp_dir / "src/{{ custom_name }}")
    fnames = ("{{ custom_name }}.txt", "titi.txt", "{{ custom_name }}/{{ custom_name }}.txt")
    for fname in fnames:
        pth = tmp_dir / "src" / fname
        pth.write_text("lorem ipsum")

    cfg = Config(DEFAULT_CFG)
    cfg._env.globals["custom_name"] = "toto"
    rg_tree = {}
    find_templates(tmp_dir / "src", tmp_dir / "tgt", cfg, rg_tree)

    fnames = ("toto.txt", "titi.txt", "toto/toto.txt")
    for fname in fnames:
        assert pth_as_key(tmp_dir / "tgt" / fname) in rg_tree


def test_find_templates_ignores_specific_names(tmp_dir):
    ensure_created(tmp_dir / "src/{{ custom_name }}")
    fnames = ("{{ custom_name }}.txt", "titi.txt", "{{ custom_name }}/{{ custom_name }}.txt")
    for fname in fnames:
        pth = tmp_dir / "src" / fname
        pth.write_text("lorem ipsum")

    cfg = Config(DEFAULT_CFG)
    cfg._env.globals["custom_name"] = "_"
    rg_tree = {}
    find_templates(tmp_dir / "src", tmp_dir / "tgt", cfg, rg_tree)

    assert pth_as_key(tmp_dir / "tgt/titi.txt") in rg_tree
    fnames = ("_.txt", "_/_.txt")
    for fname in fnames:
        assert pth_as_key(tmp_dir / "tgt" / fname) not in rg_tree


def test_find_templates_handles_src_directory_no_namespace(tmp_dir):
    pth = tmp_dir / "src/src/{{ base.pkgname }}/test.txt"
    ensure_path(pth)
    pth.write_text("lorem ipsum")

    pkg_cfg = dict(DEFAULT_CFG)
    pkg_cfg["base"] = dict(pkgname="toto", namespace=None)
    cfg = Config(pkg_cfg)
    rg_tree = {}
    find_templates(tmp_dir / "src", tmp_dir / "tgt", cfg, rg_tree)

    tgt = tmp_dir / "tgt/src/toto/test.txt"
    assert pth_as_key(tgt) in rg_tree


def test_fin_templates_handles_src_directory_with_namespace(tmp_dir):
    pth = tmp_dir / "src/src/{{ base.pkgname }}/test.txt"
    ensure_path(pth)
    pth.write_text("lorem ipsum")

    pkg_cfg = dict(DEFAULT_CFG)
    pkg_cfg["base"] = dict(pkgname="toto", namespace="myns", namespace_method="pkg_utils")
    cfg = Config(pkg_cfg)
    rg_tree = {}
    find_templates(tmp_dir / "src", tmp_dir / "tgt", cfg, rg_tree)

    tgt_dir = tmp_dir / "tgt"
    assert pth_as_key(tgt_dir / "src/myns/__init__.py") in rg_tree
    assert pth_as_key(tgt_dir / "src/myns/toto/test.txt") in rg_tree


def test_render_template_renders_file_content(tmp_dir):
    src_pth = tmp_dir / "src/test.txt"
    tgt_pth = tmp_dir / "tgt/test.txt"
    src_pth.write_text("{{ 'lorem ipsum'|upper }}")

    cfg = Config(DEFAULT_CFG)
    render_template([src_pth], tgt_pth, cfg, {})

    assert tgt_pth.read_text() == "LOREM IPSUM"


def test_render_template_overwrites_unprotected_files(tmp_dir):
    src_pth = tmp_dir / "src/test.txt"
    tgt_pth = tmp_dir / "tgt/test.txt"
    src_pth.write_text("{# pkglts, b0\n{{ random() }}\n#}\n")

    cfg = Config(DEFAULT_CFG)
    cfg._env.globals["random"] = random
    render_template([src_pth], tgt_pth, cfg, {})

    cnt0 = tgt_pth.read_text()

    render_template([src_pth], tgt_pth, cfg, {})

    cnt1 = tgt_pth.read_text()

    assert cnt0 != cnt1


def test_render_template_does_not_overwrite_protected_files(tmp_dir):
    src_pth = tmp_dir / "src/test.txt"
    tgt_pth = tmp_dir / "tgt/test.txt"
    src_pth.write_text("{# pkglts, b0\n{{ random() }}\n#}\n")

    cfg = Config(DEFAULT_CFG)
    cfg._env.globals["random"] = random
    render_template([src_pth], tgt_pth, cfg, {})

    cnt0 = tgt_pth.read_text()

    overwrite = {pth_as_key(tgt_pth): False}
    render_template([src_pth], tgt_pth, cfg, overwrite)

    cnt1 = tgt_pth.read_text()

    assert cnt0 == cnt1


def test_render_template_does_not_overwrite_outside_protected_blocks(tmp_dir):
    src_pth = tmp_dir / "src/test.txt"
    tgt_pth = tmp_dir / "tgt/test.txt"
    src_pth.write_text("{# pkglts, b0\nLOREM IPSUM\n#}\n")

    tgt_pth.write_text("Toto start\n{# pkglts, b0\nWTF?\n#}\nToto end\n")

    cfg = Config(DEFAULT_CFG)
    render_template([src_pth], tgt_pth, cfg, {})

    assert tgt_pth.read_text() == "Toto start\n{# pkglts, b0\nLOREM IPSUM\n#}\nToto end\n"
