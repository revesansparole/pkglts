import mock
from nose.tools import assert_raises

from pkglts.option.base.config import main


def test_config_is_self_sufficient():
    pkg_cfg = {}
    # call config a first time
    cfg = main(pkg_cfg, dict(pkg_fullname='mypkg',
                             owner='owner'))

    # check that a second call with the same info provided
    # first does not require user input
    new_cfg = main(pkg_cfg, cfg)

    # second has not modified options
    assert cfg == new_cfg


def test_config_use_good_defaults():
    pkg_cfg = {}
    # call config a first time
    cfg = main(pkg_cfg, dict(pkg_fullname='mypkg',
                             owner='owner'))

    # check that a second call provide right defaults
    pkg_cfg['base'] = cfg
    with mock.patch("pkglts.option_tools.loc_input", return_value=''):
        new_cfg = main(pkg_cfg, {})
        assert cfg == new_cfg


def test_config_handle_namespace():
    pkg_cfg = main({}, dict(pkg_fullname='mypkg',
                             owner='owner'))
    assert pkg_cfg['namespace'] is None
    assert pkg_cfg['pkgname'] == 'mypkg'

    pkg_cfg = main({}, dict(pkg_fullname='myns.mypkg',
                             owner='owner'))
    assert pkg_cfg['namespace'] == 'myns'
    assert pkg_cfg['pkgname'] == 'mypkg'


def test_config_check_pkg_names():
    for pkg in ('1mypkg', ' mypkg', '1', '1.mypkg',
                ' .mypkg', '.mypkg', 'None.mypkg', 'oa.o.mypkg'):
        assert_raises(UserWarning, lambda: main({}, {'pkg_fullname': pkg}))
