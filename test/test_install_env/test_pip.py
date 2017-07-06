import pytest

from pkglts.install_env.pip_front_end import install, installed_packages

from .venv_tools import clear_venv, create_venv

__test__ = False


@pytest.fixture()
def venv():
    name = "tyti_pip"
    mem = {}

    create_venv(venv, mem)

    yield name

    clear_venv(venv, mem)


def test_installed_packages():
    pkgs = set(installed_packages())
    assert "wheel" in pkgs


def test_install(venv):
    # create virtualenv
    assert "my-first-p" not in installed_packages()

    # install local wheel
    install("test/test_install_env/my_first_p-0.0.4-py2.py3-none-any.whl")

    # test new package still not in virtualenv
    assert "my-first-p" in installed_packages()
