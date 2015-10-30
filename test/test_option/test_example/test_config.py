from nose.tools import assert_raises, with_setup
import mock
from os import chdir, mkdir
from os.path import exists
from shutil import rmtree

from pkglts.option.example.config import main


tmp_dir = "tmp_cfgex"


def setup_func():
    if not exists(tmp_dir):
        mkdir(tmp_dir)

    chdir(tmp_dir)


def teardown_func():
    chdir("..")
    if exists(tmp_dir):
        rmtree(tmp_dir)


def test_config_returns_none():
    pkg_cfg = {}
    # call config a first time
    cfg = main(pkg_cfg, dict(option_name=None))

    assert cfg is None


def test_config_returns_none_if_option_not_already_installed():
    pkg_cfg = {}
    # call config a first time
    cfg = main(pkg_cfg, dict(option_name='toto'))

    assert cfg is None


def test_config_check_tempering_of_files():
    count = [0]

    def temper(*args):
        count[0] += 1

    def temper_nothing(*args):
        pass

    pkg_cfg = dict(base=dict(pkg_fullname='toto',
                             pkgname='toto',
                             namespace=None))
    with mock.patch("pkglts.option.example.config.check_tempering",
                    new=temper):
        with mock.patch("pkglts.option.example.config.regenerate_dir",
                        new=temper_nothing):
            main(pkg_cfg, dict(option_name='base'))

    assert count[0] == 1


def test_config_copy_files():
    count = [0]

    def temper(*args):
        count[0] += 1

    def temper_nothing(*args):
        pass

    pkg_cfg = dict(base=dict(pkg_fullname='toto',
                             pkgname='toto',
                             namespace=None),
                   hash={})
    with mock.patch("pkglts.option.example.config.regenerate_dir",
                    new=temper):
        with mock.patch("pkglts.option.example.config.check_tempering",
                        new=temper_nothing):
            main(pkg_cfg, dict(option_name='base'))

    assert count[0] == 1


@with_setup(setup_func, teardown_func)
def test_config_do_not_overwrite_files():
    pkg_cfg = dict(base=dict(pkg_fullname='toto',
                             pkgname='toto',
                             namespace=None),
                   hash={})

    # create files
    main(pkg_cfg, dict(option_name='base'))

    # check that rewriting them raises error
    assert_raises(UserWarning, lambda: main(pkg_cfg, dict(option_name='base')))
