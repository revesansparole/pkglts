import pytest

from pkglts.option.doc import fmt_badge


def test_fmt_badge_works_correctly():
    badge = "mybadge"
    url = "myurl"
    txt = "mytxt"

    sec = fmt_badge(badge, url, txt, 'md')
    assert badge in sec
    assert url in sec
    assert txt in sec

    sec = fmt_badge(badge, url, txt, 'rst')
    assert badge in sec
    assert url in sec
    assert txt in sec

    with pytest.raises(UserWarning):
        fmt_badge(badge, url, txt, 'docx')
