from pkglts.option.test.handlers import twice


def test_handlers():
    txt = twice("txt", {})
    assert txt == "txttxt"
