import pytest

from pkglts.option.doc.badge import Badge


def test_fmt_badge_works_correctly():
    badge = Badge(name="mybadge",
                  url="myurl",
                  url_img="myurl/img.svg",
                  text="mytxt",
                  )

    sec = badge.format('md')
    assert badge.url in sec
    assert badge.url_img in sec
    assert badge.text in sec

    sec = badge.format('rst')
    assert badge.url in sec
    assert badge.url_img in sec
    assert badge.text in sec

    with pytest.raises(UserWarning):
        badge.format('docx')
