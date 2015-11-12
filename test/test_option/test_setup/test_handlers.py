import json
from nose.tools import assert_raises, with_setup
from os import chdir, mkdir
from os.path import exists
from shutil import rmtree

from pkglts.option.setup.handlers import (get_extra, get_url,
                                          mapping,
                                          requirements, install_requirements,
                                          dvlpt_requirements)

tmp_dir = "tmp_hpydist"


def setup_func():
    if not exists(tmp_dir):
        mkdir(tmp_dir)

    chdir(tmp_dir)


def teardown_func():
    chdir("..")
    if exists(tmp_dir):
        rmtree(tmp_dir)


def test_handlers():
    assert len(mapping) == 4


def test_requirements():
    pkg_cfg = {}
    assert requirements(pkg_cfg, 'install') == "\n" * 2


def test_requirements_error_for_bad_options():
    pkg_cfg = {'toto': {}}
    assert_raises(KeyError, lambda: requirements(pkg_cfg, 'dvlpt'))


def test_install_requirements_get_install_requirements():
    pkg_cfg = {'base': {}}
    assert install_requirements("txt", pkg_cfg) == "\n" * 2


def test_dvlpt_requirements_get_dvlpt_requirements():
    pkg_cfg = {'test': {}}
    assert "nose" in dvlpt_requirements("txt", pkg_cfg)


def test_get_url_return_empty_default():
    pkg_cfg = {}
    assert get_url("txt", pkg_cfg) == ""


# TODO bug corrections self referencing tests
def test_get_url_return_base_url():
    pkg_cfg = dict(base={'url': 'base'})
    assert get_url("txt", pkg_cfg) == "base"
    pkg_cfg["github"] = {'url': 'github'}
    assert get_url("txt", pkg_cfg) == "base"
    pkg_cfg["base"]['url'] = None
    assert get_url("txt", pkg_cfg) == "github"


def test_get_url_look_multiple_places():
    for name in ("base", "github", "pypi", "readthedocs"):
        pkg_cfg = {name: {'url': name}}
        assert get_url("txt", pkg_cfg) == name


def test_get_url_avoid_none_urls():
    places = ("base", "github", "pypi", "readthedocs")
    for name in places:
        pkg_cfg = dict((n, {'url': None}) for n in places)
        pkg_cfg[name]['url'] = name
        assert get_url("txt", pkg_cfg) == name


@with_setup(setup_func, teardown_func)
def test_get_extra_return_txt_if_no_extra():
    txt = get_extra("txt", {})
    assert txt == "txt"


@with_setup(setup_func, teardown_func)
def test_get_extra_read_entry_point_json():
    eps = dict(toto1=["ep1", "ep2"], toto2=["ep3"])
    with open("entry_points.json", 'w') as f:
        json.dump(eps, f)

    txt = get_extra("txt", {})

    assert "toto1" in txt
    assert "toto2" in txt
    for i in range(1, 4):
        assert "ep%d" % i in txt
