import pytest
from pkglts.config_management import Config
from pkglts.option.doc.option import OptionDoc


@pytest.fixture()
def opt():
    return OptionDoc("doc")


@pytest.fixture()
def cfg():
    return Config(dict(base={}))


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg["doc"]) == 3


def test_config_check_description_exists(opt, cfg):
    cfg["doc"] = {"description": "mydescr", "fmt": "rst", "keywords": []}
    assert cfg["doc"]["description"] == "mydescr"
    assert "doc.description" not in opt.check(cfg)


def test_config_check_description_valid(opt, cfg):
    cfg["doc"] = {"description": "", "fmt": "rst", "keywords": []}
    assert "doc.description" in opt.check(cfg)


def test_config_check_keywords_exists(opt, cfg):
    cfg["doc"] = {"description": "mydescr", "fmt": "rst", "keywords": []}
    assert len(cfg["doc"]["keywords"]) == 0
    assert "doc.keywords" not in opt.check(cfg)


def test_config_check_fmt_valid(opt, cfg):
    cfg["doc"] = {"description": "mydescr", "fmt": "walou", "keywords": []}
    assert "doc.fmt" in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    cfg["doc"] = {"fmt": "rst"}

    assert len(tuple(opt.require(cfg))) == 0

    cfg["doc"] = {"fmt": "md"}
    assert len(tuple(opt.require(cfg))) == 1
