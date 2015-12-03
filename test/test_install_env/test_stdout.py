from nose.tools import with_setup

from pkglts.install_env.stdout_front_end import install, installed_packages

from .venv_tools import activate_venv, clear_venv, create_venv


venv = "tyti_stdout"


def setup_func():
    create_venv(venv)


def teardown_func():
    clear_venv(venv)


def test_installed_packages():
    pkgs = set(installed_packages())
    assert "pkglts" in pkgs


@with_setup(setup_func, teardown_func)
def test_install():
    # create virtualenv
    activate_venv(venv)
    assert "my-first-p" not in installed_packages()

    # install local wheel
    install("my-first-p")

    # test new package still not in virtualenv
    assert "my-first-p" not in installed_packages()
