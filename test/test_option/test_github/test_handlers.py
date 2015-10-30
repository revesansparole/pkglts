from nose.tools import with_setup
from os import chdir, mkdir
from os.path import exists
from shutil import rmtree

from pkglts.option.github.handlers import get_extra, mapping


tmp_dir = "tmp_hgithub"


def setup_func():
    if not exists(tmp_dir):
        mkdir(tmp_dir)

    chdir(tmp_dir)


def teardown_func():
    chdir("..")
    if exists(tmp_dir):
        rmtree(tmp_dir)


def test_handlers():
    assert len(mapping) == 1


@with_setup(setup_func, teardown_func)
def test_get_extra_return_txt_if_no_extra():
    txt = get_extra("txt", {})
    assert txt == "txt"


@with_setup(setup_func, teardown_func)
def test_get_extra_gitignore_extra():
    items = ["it%d" % i for i in range(10)]
    with open(".gitignore.extra", 'w') as f:
        f.write("\n".join(items))

    txt = get_extra("txt", {})

    for i in range(10):
        assert "it%d" % i in txt
