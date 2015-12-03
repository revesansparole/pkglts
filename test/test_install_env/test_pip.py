from nose.tools import with_setup

from pkglts.install_env.pip_front_end import install, installed_packages

from .venv_tools import clear_venv, create_venv


venv = "tyti_pip"
mem = {}


def setup_func():
    create_venv(venv, mem)


def teardown_func():
    clear_venv(venv, mem)


def test_installed_packages():
    pkgs = set(installed_packages())
    assert "pkglts" in pkgs


@with_setup(setup_func, teardown_func)
def test_install():
    # create virtualenv
    assert "my-first-p" not in installed_packages()

    # install local wheel
    install("test/test_install_env/my_first_p-0.0.4-py2.py3-none-any.whl")

    # test new package still not in virtualenv
    assert "my-first-p" in installed_packages()
