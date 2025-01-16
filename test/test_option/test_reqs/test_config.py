import pytest
from pkglts.config_management import Config
from pkglts.dependency import Dependency
from pkglts.option.reqs.option import OptionReqs, fmt_conda_reqs, fmt_pip_reqs, requirements


@pytest.fixture()
def opt():
    return OptionReqs("reqs")


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg["reqs"]) == 1


def test_config_check_pkg_names(opt, cfg):
    cfg["reqs"] = {"require": []}
    assert "reqs.require" not in opt.check(cfg)

    cfg["reqs"] = {"require": [{"pkg_mng": "walou", "name": "numpy"}]}
    assert "reqs.require" in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0


def test_require_puts_list_of_reqs_in_requirements(opt, cfg):
    opt.update_parameters(cfg)
    cfg["reqs"]["require"].append({"pkg_mng": "walou", "name": "numpy"})

    assert "numpy" in (dep.name for dep in requirements(cfg))


def test_fmt_conda_reqs_works_correctly():
    assert fmt_conda_reqs([], ["install"]) == ""

    d1 = Dependency("d1")
    dex = Dependency("dex", intent="example")
    dconda = Dependency("dconda")
    dpip = Dependency("dpip")

    cmd = fmt_conda_reqs([d1, dex, dconda, dpip], ["install"])

    assert cmd.strip() == "conda install d1 dconda dpip"

    d = Dependency("d", channel="extra")

    assert fmt_conda_reqs([d], ["install"]) == "conda install -c extra d"

    d = Dependency("d", version="= 5")

    assert fmt_conda_reqs([d], ["install"]) == 'conda install "d= 5"'


def test_fmt_pip_reqs_works_correctly():
    assert fmt_pip_reqs([], ["install"]) == ""

    d1 = Dependency("d1")
    dex = Dependency("dex", intent="example", pkg_mng="pip")
    dconda = Dependency("dconda")
    dpip = Dependency("dpip", pkg_mng="pip")

    cmd = fmt_pip_reqs([d1, dex, dconda, dpip], ["install"])

    assert cmd.strip() == 'pip install "dpip"'

    d = Dependency("d", pkg_mng="pip", version="= 5")

    assert fmt_pip_reqs([d], ["install"]) == 'pip install "d== 5"'
