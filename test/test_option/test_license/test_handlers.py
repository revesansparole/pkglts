from pkglts.option.license.handlers import generate, setup_handler


def test_generate():
    cfg = dict(name='mit',
               year="2015",
               organization="org",
               project="project")
    txt = generate("txt", dict(license=cfg))
    assert len(txt) > 0
    assert txt != "txt"


def test_setup():
    cfg = dict(name='mit',
               year="2015",
               organization="org",
               project="project")
    txt = setup_handler("txt", dict(license=cfg))
    assert len(txt) > 0
    assert txt != "txt"
