import mock

from pkglts.option.doc.handlers import (badges,
                                              leading_list, contributing_list,
                                              history)


def test_badges():
    assert badges("txt", {}) == "txt"


# def test_badges_sans_github():
#     with mock.patch("pkglts.option.doc.readme.badges",
#                     side_effect=ImportError):
#         assert badges("txt", dict(github={})) == "txt"


def test_badges_number():
    web_services = ("readthedocs", "travis", "coveralls", "landscape")
    pkg_cfg = dict((name, {}) for name in web_services)
    pkg_cfg["base"] = dict(owner='toto')
    pkg_cfg["github"] = dict(project='project')
    txt = badges("txt", pkg_cfg)
    assert txt.count(".. image::") == len(web_services)


def test_leading_list():
    assert leading_list("txt", {}) == "txt"


def test_leading_list_none():
    with mock.patch("pkglts.option.doc.authors.fetch_contributors",
                    return_value=None):
        assert leading_list("txt", dict(github={})) == "txt"


def test_leading_list_fmt():
    with mock.patch("pkglts.option.doc.authors.fetch_contributors",
                    return_value=[("to", "to")] * 4):
        assert len(leading_list("txt", dict(github={})).split("\n")) == 4


def test_contributing_list():
    assert contributing_list("txt", {}) == "txt"


def test_history():
    assert history("txt", {}) == "txt"


def test_history_none():
    with mock.patch("pkglts.option.doc.history.fetch_history",
                    return_value=None):
        assert history("txt", dict(github={})) == "txt"


def test_history_fmt():
    with mock.patch("pkglts.option.doc.history.fetch_history",
                    return_value=["toto"] * 4):
        assert len(history("txt", dict(github={})).split("\n")) == 4

