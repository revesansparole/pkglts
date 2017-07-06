import pytest

from pkglts.install_env.load_front_end import get_install_front_end


def test_load_stdout_exists():
    ife = get_install_front_end('stdout')
    assert hasattr(ife, "install")


def test_load_pip_exists():
    ife = get_install_front_end('pip')
    assert hasattr(ife, "install")


def test_load_raise_import_error_if_not_available_name():
    with pytest.raises(ImportError):
        get_install_front_end("takapouet")
