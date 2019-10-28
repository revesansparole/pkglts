import pytest
from pkglts.config_management import Config
from pkglts.dependency import Dependency
from pkglts.option.reqs.option import OptionReqs, fmt_conda_reqs, fmt_pip_reqs


@pytest.fixture()
def opt():
    return OptionReqs('reqs')


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['reqs']) == 1


def test_config_check_pkg_names(opt):
    cfg = Config(dict(reqs={'require': []}))
    assert 'reqs.require' not in opt.check(cfg)

    cfg = Config(dict(reqs={'require': [{'pkg_mng': 'walou', 'name': 'numpy'}]}))
    assert 'reqs.require' in opt.check(cfg)


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0


def test_fmt_conda_reqs_works_correctly():
    assert fmt_conda_reqs([], ['install']) == ""

    d1 = Dependency('d1')
    dex = Dependency('dex', intent='example')
    dconda = Dependency('dconda')
    dpip = Dependency('dpip')

    cmd = fmt_conda_reqs([d1, dex, dconda, dpip], ['install'])

    assert cmd.strip() == "conda install d1 dconda dpip"

    d = Dependency('d', channel='extra')

    assert fmt_conda_reqs([d], ['install']) == "conda install -c extra d"


def test_fmt_pip_reqs_works_correctly():
    assert fmt_pip_reqs([], ['install']) == ""

    d1 = Dependency('d1')
    dex = Dependency('dex', intent='example', pkg_mng='pip')
    dconda = Dependency('dconda')
    dpip = Dependency('dpip', pkg_mng='pip')

    cmd = fmt_pip_reqs([d1, dex, dconda, dpip], ['install'])

    assert cmd.strip() == "pip install dpip"
