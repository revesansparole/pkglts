from nose.tools import with_setup
from os import mkdir
from os.path import dirname, exists
from os.path import join as pj
from shutil import rmtree

from pkglts.manage_tools import regenerate_file, regenerate_pkg


print(__file__)


tmp_dir = "takapouet"


def setup():
    if not exists(tmp_dir):
        mkdir(tmp_dir)


def teardown():
    if exists(tmp_dir):
        rmtree(tmp_dir)


def ensure_path(pth):
    dname = dirname(pth)
    if not exists(dname):
        ensure_path(dname)
        mkdir(dname)


@with_setup(setup, teardown)
def test_regenerate_file_replace_divs():
    fname = pj(tmp_dir, "test.py")
    ref_txt = "# {{upper, toto}}"
    with open(fname, 'w') as f:
        f.write(ref_txt)

    regenerate_file(fname, {}, {})

    with open(fname, 'r') as f:
        assert f.read() != ref_txt


@with_setup(setup, teardown)
def test_regenerate_pkg_walk_all_files_by_default():
    ref_txt = "# {{upper, toto}}"
    pths = [pj(tmp_dir, n) for n in ("test1.py", "test2.py",
                                     "tot/test3.py", "tot/test4.py")]

    for pth in pths:
        ensure_path(pth)
        with open(pth, 'w') as f:
            f.write(ref_txt)

    regenerate_pkg({}, {}, tmp_dir, {})

    for pth in pths:
        with open(pth, 'r') as f:
            assert f.read() != ref_txt


@with_setup(setup, teardown)
def test_regenerate_pkg_exclude_protected_dirs():
    ref_txt = "# {{upper, toto}}"
    pths = [pj(tmp_dir, n) for n in ("test1.py", "test2.py",
                                     "tot/test3.py", "tot/test4.py")]

    for pth in pths:
        ensure_path(pth)
        with open(pth, 'w') as f:
            f.write(ref_txt)

    with open(pj(tmp_dir, "tot", "regenerate.no"), 'w') as f:
        f.write("")

    regenerate_pkg({}, {}, tmp_dir, {})

    for pth in pths[:2]:
        with open(pth, 'r') as f:
            assert f.read() != ref_txt

    for pth in pths[2:]:
        with open(pth, 'r') as f:
            assert f.read() == ref_txt


@with_setup(setup, teardown)
def test_regenerate_pkg_exclude_hidden_dirs():
    ref_txt = "# {{upper, toto}}"
    pths = [pj(tmp_dir, n) for n in ("test1.py", "test2.py",
                                     ".tot/test3.py", ".tot/test4.py")]

    for pth in pths:
        ensure_path(pth)
        with open(pth, 'w') as f:
            f.write(ref_txt)

    regenerate_pkg({}, {}, tmp_dir, {})

    for pth in pths[:2]:
        with open(pth, 'r') as f:
            assert f.read() != ref_txt

    for pth in pths[2:]:
        with open(pth, 'r') as f:
            assert f.read() == ref_txt


@with_setup(setup, teardown)
def test_regenerate_pkg_exclude_protected_files():
    ref_txt = "# {{upper, toto}}"
    pths = [pj(tmp_dir, n).replace("\\", "/")
            for n in ("test1.py", "test2.py", "tot/test3.py", "tot/test4.py")]

    for pth in pths:
        ensure_path(pth)
        with open(pth, 'w') as f:
            f.write(ref_txt)

    regenerate_pkg({}, {}, tmp_dir, dict((pth, False) for pth in pths[1:3]))

    for pth in pths[1:3]:
        with open(pth, 'r') as f:
            assert f.read() == ref_txt

    for pth in pths[:1] + pths[3:]:
        with open(pth, 'r') as f:
            assert f.read() != ref_txt


# @with_setup(setup, teardown)
# def test_regenerate_walk_files_in_ltpkgbuilder_data():
#     pkg_cfg = {'hash': {}}
#     handlers = {}
#
#     regenerate_dir("pkglts_data/test/test1", tmp_dir, handlers, pkg_cfg)
#
#     ref_fnames = {"titi.txt", "tutu.txt", "subtest"}
#
#     crt_fnames = set()
#     for r, ds, fs in walk(tmp_dir):
#         crt_fnames.update(ds)
#         crt_fnames.update(fs)
#
#     assert ref_fnames == crt_fnames
#
#
# @with_setup(setup, teardown)
# def test_regenerate_walk_files_except_pyc():
#     pkg_cfg = {'hash': {}}
#     handlers = {}
#
#     regenerate_dir("pkglts_data/test/test3", tmp_dir, handlers, pkg_cfg)
#
#     ref_fnames = {"titi.txt", "tutu.txt", "subtest"}
#
#     crt_fnames = set()
#     for r, ds, fs in walk(tmp_dir):
#         crt_fnames.update(ds)
#         crt_fnames.update(fs)
#
#     assert ref_fnames == crt_fnames
#
#
# @with_setup(setup, teardown)
# def test_regenerate_replace_directory_names():
#     pkg_cfg = {'hash': {}}
#     handlers = {}
#
#     regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)
#
#     assert not exists(tmp_dir + "/{{rm, tok}}tok")
#     assert exists(tmp_dir + "/tok")
#     assert not exists(tmp_dir + "/{{toto, tik}}tik")
#     assert exists(tmp_dir + "/tiktik")
#
#
# @with_setup(setup, teardown)
# def test_regenerate_do_not_create_directory_with_empty_name():
#     pkg_cfg = {'hash': {}}
#     handlers = {}
#
#     regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)
#
#     assert not exists(tmp_dir + "/{{rm, tak}}")
#     assert not exists(tmp_dir + "/tak")
#
#
# @with_setup(setup, teardown)
# def test_regenerate_replace_file_names():
#     pkg_cfg = {'hash': {}}
#     handlers = {'doc': same}
#
#     regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)
#
#     assert not exists(tmp_dir + "/{{rm, ta}}ta.txt")
#     assert not exists(tmp_dir + "/tata.txt")
#     assert exists(tmp_dir + "/ta.txt")
#
#
# @with_setup(setup, teardown)
# def test_regenerate_do_not_create_file_with_empty_name():
#     pkg_cfg = {'hash': {}}
#     handlers = {'doc': same}
#
#     regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)
#
#     assert not exists(tmp_dir + "/tok/{{del, toto.txt}}")
#     assert not exists(tmp_dir + "/tok/toto.txt")
#     assert not exists(tmp_dir + "/tok/{{del, titi}}.txt")
#     assert not exists(tmp_dir + "/tok/titi.txt")
#     assert len(listdir(tmp_dir + "/tok")) == 0
#
#
# @with_setup(setup, teardown)
# def test_regenerate_replace_file_content():
#     pkg_cfg = {'hash': {}}
#     handlers = {'upper': lambda s, env: s.upper()}
#
#     regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)
#
#     assert exists(tmp_dir + "/tutu.txt")
#     with open(tmp_dir + "/tutu.txt", 'r') as f:
#         txt = f.read()
#         assert txt == "lorem ipsum NOTHING lorem ipsum"
#
#
# @with_setup(setup, teardown)
# def test_regenerate_handle_src_directory_no_namespace():
#     pkg_cfg = {'hash': {}, 'base': {'namespace': None, 'pkgname': 'mypkg'}}
#     handlers = {'base': same}
#
#     regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)
#
#     assert exists(tmp_dir + "/src")
#     assert exists(tmp_dir + "/src/mypkg")
#
#
# @with_setup(setup, teardown)
# def test_regenerate_handle_src_directory_with_namespace():
#     pkg_cfg = {'hash': {}, 'base': {'namespace': 'myns', 'pkgname': 'mypkg'}}
#     handlers = {'base': same}
#
#     regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)
#
#     assert exists(tmp_dir + "/src")
#     assert exists(tmp_dir + "/src/myns")
#     assert exists(tmp_dir + "/src/myns/__init__.py")
#     assert exists(tmp_dir + "/src/myns/mypkg")
