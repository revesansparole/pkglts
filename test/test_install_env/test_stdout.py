from pkglts.install_env.stdout_front_end import install, installed_packages


def test_installed_packages():
    pkgs = set(installed_packages())
    assert "pkglts" in pkgs


def test_install():
    # create virtualenv
    pass
    # assert "bla" not in installed_packages()

    # install local wheel
    # install("bla", params)

    # test new package still not in virtualenv
    # assert "bla" not in installed_packages()
