from pkglts.templating import parse_source


def test_parse_finds_all_blocks():
    txt = "assert 'toto'\n" "assert 'titi'\n" "# {# pkglts, bid\n" "this is content\n" "# #}\n" "after block"
    blocks = parse_source(txt)
    assert len(blocks) == 3
    b1, b2, b3 = blocks
    assert b1.before_header == ""
    assert b1.bid is None
    assert b1.after_header == ""
    assert b1.content == ("assert 'toto'\n" "assert 'titi'\n")
    assert b1.before_footer == ""
    assert b1.after_footer == ""

    assert b2.before_header == "# "
    assert b2.bid == "bid"
    assert b2.after_header == ""
    assert b2.content == "this is content\n"
    assert b2.before_footer == "# "
    assert b2.after_footer == ""

    assert b3.before_header == ""
    assert b3.bid is None
    assert b3.after_header == ""
    assert b3.content == "after block"
    assert b3.before_footer == ""
    assert b3.after_footer == ""


def test_parse_finds_bef_after_header():
    txt = (
        "assert 'toto'\n"
        "assert 'titi'\n"
        "# bef header{# pkglts, bid after header\n"
        "this is content\n"
        "# #}\n"
        "after block"
    )
    blocks = parse_source(txt)
    assert len(blocks) == 3
    _, block, _ = blocks
    assert block.before_header == "# bef header"
    assert block.bid == "bid"
    assert block.after_header == " after header"
    assert block.content == "this is content\n"
    assert block.before_footer == "# "
    assert block.after_footer == ""


def test_parse_finds_bef_after_footer():
    txt = (
        "assert 'toto'\n"
        "assert 'titi'\n"
        "# {# pkglts, bid\n"
        "this is content\n"
        "# bef footer#} after footer\n"
        "after block"
    )
    blocks = parse_source(txt)
    assert len(blocks) == 3
    _, block, _ = blocks
    assert block.before_header == "# "
    assert block.bid == "bid"
    assert block.after_header == ""
    assert block.content == "this is content\n"
    assert block.before_footer == "# bef footer"
    assert block.after_footer == " after footer"


def test_parse_finds_single_pkglts_block():
    txt = "# {# pkglts, bid\n" "this is content\n" "# bef footer#} after footer\n"
    blocks = parse_source(txt)
    assert len(blocks) == 1
    (block,) = blocks
    assert block.before_header == "# "
    assert block.bid == "bid"
    assert block.after_header == ""
    assert block.content == "this is content\n"
    assert block.before_footer == "# bef footer"
    assert block.after_footer == " after footer"
