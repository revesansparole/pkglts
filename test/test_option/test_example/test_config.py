import mock

from pkglts.option.example.config import main


def test_config_returns_none():
    pkg_cfg = {}
    # call config a first time
    cfg = main(pkg_cfg, dict(option_name=None))

    assert cfg is None


def test_config_returns_none_if_option_not_already_installed():
    pkg_cfg = {}
    # call config a first time
    cfg = main(pkg_cfg, dict(option_name='toto'))

    assert cfg is None


def test_config_check_tempering_of_files():
    count = [0]

    def temper(*args):
        count[0] += 1

    def temper_nothing(*args):
        pass

    pkg_cfg = dict(base=dict(pkg_fullname='toto',
                             pkgname='toto',
                             namespace=None))
    with mock.patch("pkglts.option.example.config.check_tempering",
                    new=temper):
        with mock.patch("pkglts.option.example.config.regenerate_dir",
                        new=temper_nothing):
            main(pkg_cfg, dict(option_name='base'))

    assert count[0] == 1


def test_config_copy_files():
    count = [0]

    def temper(*args):
        count[0] += 1

    def temper_nothing(*args):
        pass

    pkg_cfg = dict(base=dict(pkg_fullname='toto',
                             pkgname='toto',
                             namespace=None),
                   hash={})
    with mock.patch("pkglts.option.example.config.regenerate_dir",
                    new=temper):
        with mock.patch("pkglts.option.example.config.check_tempering",
                        new=temper_nothing):
            main(pkg_cfg, dict(option_name='base'))

    assert count[0] == 1
