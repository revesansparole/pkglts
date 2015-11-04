import mock

from pkglts.option.version.config import main


def test_config_is_self_sufficient():
    pkg_cfg = {}
    # call config a first time
    cfg = main(pkg_cfg, dict(major="0", minor="1", post="2"))

    # check that a second call with the same info provided
    # first does not require user input
    new_cfg = main(pkg_cfg, cfg)

    # second has not modified options
    assert cfg == new_cfg


def test_config_use_good_defaults():
    pkg_cfg = {}
    # call config a first time
    cfg = main(pkg_cfg, dict(major="0", minor="1", post="2"))

    # check that a second call provide right defaults
    pkg_cfg['version'] = cfg
    with mock.patch("pkglts.option_tools.loc_input", return_value=''):
        new_cfg = main(pkg_cfg, {})
        assert cfg == new_cfg
