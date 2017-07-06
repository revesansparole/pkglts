import pytest

from pkglts.config_management import create_env
from pkglts.local import (pkg_full_name, src_dir)


print(__file__)


def test_pkg_full_name():
    cfg = {}
    with pytest.raises(KeyError):
        pkg_full_name(create_env(cfg))

    cfg['base'] = dict(pkgname='toto', namespace=None)
    name1 = pkg_full_name(create_env(cfg))
    cfg['base']['namespace'] = 'oa'
    name2 = pkg_full_name(create_env(cfg))

    assert name1 != name2


def test_src_dir():
    cfg = {}
    with pytest.raises(KeyError):
        pkg_full_name(create_env(cfg))

    cfg['base'] = dict(pkgname='toto', namespace=None)
    dir1 = src_dir(create_env(cfg))
    cfg['base']['namespace'] = 'oa'
    dir2 = src_dir(create_env(cfg))

    assert dir1 != dir2
