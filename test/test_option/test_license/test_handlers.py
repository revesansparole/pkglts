from nose.tools import assert_raises

from pkglts.option.license.handlers import generate, setup_handler


def test_generate():
    cfg = dict(name='mit',
               year="2015",
               organization="org",
               project="project")
    txt = generate("txt", dict(license=cfg))
    assert len(txt) > 0
    assert txt != "txt"


def test_generate_raise_error_if_license_do_not_exists():
    cfg = dict(name='tugudu',
               year="2015",
               organization="org",
               project="project")
    assert_raises(IOError, lambda: generate("txt", dict(license=cfg)))


def test_setup():
    cfg = dict(name='mit',
               year="2015",
               organization="org",
               project="project")
    txt = setup_handler("txt", dict(license=cfg))
    assert len(txt) > 0
    assert txt != "txt"
