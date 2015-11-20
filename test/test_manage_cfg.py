import mock
from nose.tools import assert_raises, with_setup
from os import listdir, mkdir
from os.path import exists
from hashlib import sha512
from shutil import rmtree

from pkglts.versioning import get_local_version
from pkglts.manage import (clean, get_pkg_config, get_pkg_hash,
                           init_pkg,
                           add_option, update_option, edit_option,
                           update_pkg,
                           write_pkg_config)


print(__file__)

tmp_dir = 'toto_manage_cfg'


def setup():
    if not exists(tmp_dir):
        mkdir(tmp_dir)


def teardown():
    if exists(tmp_dir):
        rmtree(tmp_dir)


@with_setup(setup, teardown)
def test_manage_init_create_pkg_config():
    init_pkg(tmp_dir)
    cfg = get_pkg_config(tmp_dir)
    assert cfg is not None
    assert "_pkglts" in cfg


@with_setup(setup, teardown)
def test_manage_init_create_pkg_hash():
    init_pkg(tmp_dir)
    hm = get_pkg_hash(tmp_dir)
    assert hm is not None


@with_setup(setup, teardown)
def test_manage_pkg_config():
    cfg = dict(toto={'toto': 1})
    write_pkg_config(cfg, tmp_dir)
    new_cfg = get_pkg_config(tmp_dir)
    assert new_cfg == cfg


# @with_setup(setup, teardown)
# def test_manage_pkg_config_fmt_templates():
#     cfg = dict(toto={'base': 10, 'toto': "{{key, base}}"})
#     write_pkg_config(cfg, tmp_dir)
#
#     cfg = get_pkg_config(tmp_dir)['toto']
#     assert 'base' in cfg
#     assert 'toto' in cfg
#     assert cfg['toto'] == "10"


@with_setup(setup, teardown)
def test_manage_cfg_store_any_item():
    algo = sha512()
    algo.update(("lorem ipsum\n" * 10).encode("latin1"))

    cfg = dict(simple=1,
               txt="lorem ipsum\n" * 4,
               hash=algo.digest().decode("latin1"))

    write_pkg_config(dict(toto=cfg), tmp_dir)

    new_cfg = get_pkg_config(tmp_dir)['toto']
    assert new_cfg == cfg

    algo = sha512()
    algo.update(("lorem ipsum\n" * 10).encode("latin1"))
    assert algo.digest() == new_cfg['hash'].encode("latin1")


@with_setup(setup, teardown)
def test_manage_cfg_do_store_private_item():
    cfg = {'toto': {}, '_toto': {}}
    write_pkg_config(cfg, tmp_dir)

    new_cfg = get_pkg_config(tmp_dir)
    assert '_toto' in new_cfg
