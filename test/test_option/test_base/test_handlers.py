from pkglts.local import src_dir
from pkglts.option.base.handlers import (upper, lower,
                                         get_src_pth, mapping, pkg_full_name)


def test_mapping():
    assert len(mapping) == 4


def test_upper():
    assert upper("toto", {}) == "TOTO"


def test_lower():
    assert lower("ToTo", {}) == "toto"


def test_get_src_pth():
    cfg = {'base': {'pkgname': 'toto', 'namespace': 'oa'}}
    assert src_dir(cfg) == get_src_pth("whatever", cfg)


def test_pkg_full_name():
    cfg = {'base': {'pkgname': 'toto', 'namespace': 'oa'}}
    assert pkg_full_name("whatever", cfg) == 'oa.toto'

    cfg = {'base': {'pkgname': 'toto', 'namespace': None}}
    assert pkg_full_name("whatever", cfg) == 'toto'
