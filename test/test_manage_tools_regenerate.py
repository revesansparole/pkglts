from nose.tools import with_setup
from os import listdir, mkdir, walk
from os.path import exists
from shutil import rmtree

from pkglts.manage_tools import regenerate_dir
from pkglts.templating import same


print(__file__)


tmp_dir = "takapouet"


def setup():
    if not exists(tmp_dir):
        mkdir(tmp_dir)


def teardown():
    if exists(tmp_dir):
        rmtree(tmp_dir)


@with_setup(setup, teardown)
def test_regenerate_walk_files_in_ltpkgbuilder_data():
    pkg_cfg = {'hash': {}}
    handlers = {}

    regenerate_dir("pkglts_data/test/test1", tmp_dir, handlers, pkg_cfg)

    ref_fnames = {"titi.txt", "tutu.txt", "subtest"}

    crt_fnames = set()
    for r, ds, fs in walk(tmp_dir):
        crt_fnames.update(ds)
        crt_fnames.update(fs)

    assert ref_fnames == crt_fnames


@with_setup(setup, teardown)
def test_regenerate_walk_files_except_pyc():
    pkg_cfg = {'hash': {}}
    handlers = {}

    regenerate_dir("pkglts_data/test/test3", tmp_dir, handlers, pkg_cfg)

    ref_fnames = {"titi.txt", "tutu.txt", "subtest"}

    crt_fnames = set()
    for r, ds, fs in walk(tmp_dir):
        crt_fnames.update(ds)
        crt_fnames.update(fs)

    assert ref_fnames == crt_fnames


@with_setup(setup, teardown)
def test_regenerate_replace_directory_names():
    pkg_cfg = {'hash': {}}
    handlers = {}

    regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)

    assert not exists(tmp_dir + "/{{rm, tok}}tok")
    assert exists(tmp_dir + "/tok")
    assert not exists(tmp_dir + "/{{toto, tik}}tik")
    assert exists(tmp_dir + "/tiktik")


@with_setup(setup, teardown)
def test_regenerate_do_not_create_directory_with_empty_name():
    pkg_cfg = {'hash': {}}
    handlers = {}

    regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)

    assert not exists(tmp_dir + "/{{rm, tak}}")
    assert not exists(tmp_dir + "/tak")


@with_setup(setup, teardown)
def test_regenerate_replace_file_names():
    pkg_cfg = {'hash': {}}
    handlers = {'doc': same}

    regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)

    assert not exists(tmp_dir + "/{{rm, ta}}ta.txt")
    assert not exists(tmp_dir + "/tata.txt")
    assert exists(tmp_dir + "/ta.txt")


@with_setup(setup, teardown)
def test_regenerate_do_not_create_file_with_empty_name():
    pkg_cfg = {'hash': {}}
    handlers = {'doc': same}

    regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)

    assert not exists(tmp_dir + "/tok/{{del, toto.txt}}")
    assert not exists(tmp_dir + "/tok/toto.txt")
    assert not exists(tmp_dir + "/tok/{{del, titi}}.txt")
    assert not exists(tmp_dir + "/tok/titi.txt")
    assert len(listdir(tmp_dir + "/tok")) == 0


@with_setup(setup, teardown)
def test_regenerate_replace_file_content():
    pkg_cfg = {'hash': {}}
    handlers = {'upper': lambda s, env: s.upper()}

    regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)

    assert exists(tmp_dir + "/tutu.txt")
    with open(tmp_dir + "/tutu.txt", 'r') as f:
        txt = f.read()
        assert txt == "lorem ipsum NOTHING lorem ipsum"


@with_setup(setup, teardown)
def test_regenerate_handle_src_directory_no_namespace():
    pkg_cfg = {'hash': {}, 'base': {'namespace': None, 'pkgname': 'mypkg'}}
    handlers = {'base': same}

    regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)

    assert exists(tmp_dir + "/src")
    assert exists(tmp_dir + "/src/mypkg")


@with_setup(setup, teardown)
def test_regenerate_handle_src_directory_with_namespace():
    pkg_cfg = {'hash': {}, 'base': {'namespace': 'myns', 'pkgname': 'mypkg'}}
    handlers = {'base': same}

    regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)

    assert exists(tmp_dir + "/src")
    assert exists(tmp_dir + "/src/myns")
    assert exists(tmp_dir + "/src/myns/__init__.py")
    assert exists(tmp_dir + "/src/myns/mypkg")
