import pytest

from pkglts.install_env.stdout_front_end import install, installed_packages

from .venv_tools import clear_venv, create_venv

__test__ = False


@pytest.fixture()
def venv():
    name = "tyti_stdout"
    mem = {}

    create_venv(venv, mem)

    yield name

    clear_venv(venv, mem)


def test_installed_packages():
    pkgs = set(installed_packages())
    assert "pkglts" in pkgs


def test_install(venv):
    assert "my-first-p" not in installed_packages()

    # install local wheel
    install("my-first-p")

    # test new package still not in virtualenv
    assert "my-first-p" not in installed_packages()
