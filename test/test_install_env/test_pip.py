from pkglts.install_env.pip_front_end import install, installed_packages


def test_installed_packages():
    pkgs = set(installed_packages())
    assert "pkglts" in pkgs


def test_install():
    # create virtualenv
    pass
    # assert "bla" not in installed_packages()

    # install local wheel
    # install("bla", params)

    # test new package in virtualenv
    # assert "bla" in installed_packages()
