from pkglts.local import src_dir
from pkglts.option.base.handlers import upper, lower, get_src_pth


def test_upper():
    assert upper("toto", {}) == "TOTO"


def test_lower():
    assert lower("ToTo", {}) == "toto"


def test_get_src_pth():
    cfg = {'base': {'pkgname': 'toto', 'namespace': 'oa'}}
    assert src_dir(cfg) == get_src_pth("whatever", cfg)
