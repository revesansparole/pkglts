from pkglts.option.doc.handlers import fmt_keywords, mapping


def test_mapping():
    assert len(mapping) == 1


def test_fmt_keywords():
    cfg = dict(doc={'keywords': ['toto', 'titi']})
    assert fmt_keywords("ttu", cfg) == 'toto, titi'
