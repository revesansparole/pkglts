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

tmp_dir = 'toto_local'


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


@with_setup(setup, teardown)
def test_manage_init_create_pkg_hash():
    init_pkg(tmp_dir)
    hm = get_pkg_hash(tmp_dir)
    assert hm is not None


@with_setup(setup, teardown)
def test_manage_pkg_config():
    cfg = {'toto': 1}
    write_pkg_config(cfg, tmp_dir)
    new_cfg = get_pkg_config(tmp_dir)
    assert new_cfg == cfg


@with_setup(setup, teardown)
def test_manage_cfg_store_any_item():
    algo = sha512()
    algo.update(("lorem ipsum\n" * 10).encode("latin1"))

    cfg = dict(simple=1,
               txt="lorem ipsum\n" * 4,
               hash=algo.digest().decode("latin1"))

    write_pkg_config(cfg, tmp_dir)

    new_cfg = get_pkg_config(tmp_dir)
    assert new_cfg == cfg

    algo = sha512()
    algo.update(("lorem ipsum\n" * 10).encode("latin1"))
    assert algo.digest() == new_cfg['hash'].encode("latin1")


@with_setup(setup, teardown)
def test_manage_cfg_do_not_store_private_item():
    cfg = {'toto': {}, '_toto': {}}
    write_pkg_config(cfg, tmp_dir)

    new_cfg = get_pkg_config(tmp_dir)
    assert '_toto' not in new_cfg


@with_setup(setup, teardown)
def test_clean_remove_pyc_files():
    name = tmp_dir + "/" + "toto.pyc"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert not exists(name)


@with_setup(setup, teardown)
def test_clean_remove_pycache_directories():
    pycache = tmp_dir + "/" + "__pycache__"
    mkdir(pycache)
    name = pycache + "/" + "toto.py"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert not exists(pycache)
    assert not exists(name)


@with_setup(setup, teardown)
def test_clean_do_not_remove_py_files():
    name = tmp_dir + "/" + "toto.py"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert exists(name)


@with_setup(setup, teardown)
def test_clean_do_not_remove_hidden_files():
    name = tmp_dir + "/" + ".toto.pyc"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert exists(name)


@with_setup(setup, teardown)
def test_clean_do_not_explore_hidden_directories():
    hidden = tmp_dir + "/" + ".test"
    mkdir(hidden)
    name = hidden + "/" + "toto.py"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert exists(hidden)
    assert exists(name)


@with_setup(setup, teardown)
def test_clean_do_not_explore_clean_no_directories():
    hidden = tmp_dir + "/" + "test"
    mkdir(hidden)
    name = hidden + "/" + "toto.py"
    with open(name, 'w') as f:
        f.write("toto")

    with open(hidden + "/" + "clean.no", 'w') as f:
        f.write("")

    clean(tmp_dir)
    assert exists(hidden)
    assert exists(name)


@with_setup(setup, teardown)
def test_clean_remove_dist_build_directories():
    for name in ("dist", "build"):
        mkdir(tmp_dir + "/" + name)

    clean(tmp_dir)
    assert len(listdir(tmp_dir)) == 0


def test_add_already_existing_option_raises_warning():
    pkg_cfg = add_option('base', {}, extra={'pkg_fullname': 'toto',
                                            'owner': 'owner'})
    assert_raises(UserWarning, lambda: add_option('base', pkg_cfg))


def test_manage_update_pkg_do_nothing_if_up_to_date():
    pkg_cfg = update_pkg({})
    assert len(pkg_cfg) == 0


def test_manage_update_pkg_do_not_change_installed_options():
    ver = get_local_version()
    ver.version = (ver.version[0], ver.version[1] + 1, ver.version[2])

    pkg_cfg = {'base': dict(pkg_fullname='toto',
                            pkgname='toto',
                            namespace=None,
                            owner='owner')}

    mem = dict(pkg_cfg['base'])

    with mock.patch("pkglts.manage.get_github_version",
                    return_value=ver):
        with mock.patch('pkglts.option_tools.loc_input',
                        return_value=''):
            pkg_cfg = update_pkg(pkg_cfg)
            assert len(pkg_cfg) == 1
            assert pkg_cfg['base'] == mem


def test_manage_update_pkg_requires_user_input():
    ver = get_local_version()
    ver.version = (ver.version[0], ver.version[1] + 1, ver.version[2])

    pkg_cfg = {'base': dict(pkg_fullname='toto',
                            pkgname='toto',
                            namespace=None,
                            owner='owner')}

    mem = dict(pkg_cfg['base'])

    with mock.patch("pkglts.manage.get_github_version",
                    return_value=ver):
        with mock.patch('pkglts.option_tools.loc_input',
                        return_value='n'):
            pkg_cfg['toto'] = dict(option=None)
            pkg_cfg = update_pkg(pkg_cfg)
            assert len(pkg_cfg) == 2
            assert pkg_cfg['base'] == mem


def test_manage_update_opt_raise_error_if_not_already_installed():
    pkg_cfg = {}
    assert_raises(UserWarning, lambda: update_option('base', pkg_cfg))


def test_manage_update_same_opt_do_not_change_anything():
    pkg_cfg = {'hash': {}}
    pkg_cfg = add_option('base', pkg_cfg, {"pkg_fullname": 'toto',
                                           'owner': 'owner'})

    mem = dict(pkg_cfg['base'])
    pkg_cfg = update_option('base', pkg_cfg)
    assert mem == pkg_cfg['base']


def test_manage_edit_opt_raise_error_if_not_already_installed():
    pkg_cfg = {}
    assert_raises(UserWarning, lambda: edit_option('base', pkg_cfg))


def test_manage_edit_opt_with_defaults_do_not_change_anything():
    pkg_cfg = {'hash': {}}
    pkg_cfg = add_option('base', pkg_cfg, {"pkg_fullname": 'toto',
                                           'owner': 'owner'})

    mem = dict(pkg_cfg['base'])
    with mock.patch('pkglts.option_tools.loc_input', return_value=''):
        pkg_cfg = edit_option('base', pkg_cfg)
        assert mem == pkg_cfg['base']
