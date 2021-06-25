import pytest
from pkglts.config_management import Config
from pkglts.option.pypi.option import OptionPypi


@pytest.fixture()
def opt():
    return OptionPypi('pypi')


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg['pypi']) == 2


def test_config_check_classifiers_exists(opt, cfg):
    cfg['pypi'] = {'classifiers': []}
    assert 'pypi.classifiers' in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 2


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 1
