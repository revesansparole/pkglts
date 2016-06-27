from nose.tools import assert_raises

from pkglts.config_management import create_env
from pkglts.local import (pkg_full_name, src_dir)


print(__file__)


def test_pkg_full_name():
    cfg = {}
    assert_raises(KeyError, lambda: pkg_full_name(create_env(cfg)))

    cfg['base'] = dict(pkgname='toto', namespace=None)
    name1 = pkg_full_name(create_env(cfg))
    cfg['base']['namespace'] = 'oa'
    name2 = pkg_full_name(create_env(cfg))

    assert name1 != name2


def test_src_dir():
    cfg = {}
    assert_raises(KeyError, lambda: src_dir(create_env(cfg)))

    cfg['base'] = dict(pkgname='toto', namespace=None)
    dir1 = src_dir(create_env(cfg))
    cfg['base']['namespace'] = 'oa'
    dir2 = src_dir(create_env(cfg))

    assert dir1 != dir2
