from pkglts.option.tox.handlers import pyversions


def test_handlers():
    pkg_cfg = dict(setup={'intended_versions': ["27"]})
    txt = pyversions("txt", pkg_cfg)
    assert txt != "txt"
