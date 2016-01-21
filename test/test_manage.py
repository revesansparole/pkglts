import mock
from nose.tools import assert_raises

from pkglts.versioning import get_local_version
from pkglts.manage import (add_option, default_cfg, update_option, edit_option,
                           update_pkg)


def test_manage_update_pkg_do_nothing_if_up_to_date():
    pkg_cfg = update_pkg({})
    assert len(pkg_cfg) == 0


def test_manage_update_pkg_do_not_change_installed_options():
    ver = get_local_version()
    ver.version = (ver.version[0], ver.version[1] + 1, ver.version[2])

    pkg_cfg = dict(default_cfg)
    pkg_cfg['base'] = dict(pkgname='toto',
                           namespace=None,
                           owner='owner',
                           url=None)

    mem = dict(pkg_cfg['base'])
    nb = len(pkg_cfg)

    with mock.patch("pkglts.manage.get_github_version",
                    return_value=ver):
        with mock.patch('pkglts.option_tools.loc_input',
                        return_value=''):
            pkg_cfg = update_pkg(pkg_cfg)
            assert len(pkg_cfg) == nb
            assert pkg_cfg['base'] == mem


def test_manage_add_opt_raise_error_if_already_installed():
    pkg_cfg = dict(default_cfg)
    pkg_cfg = add_option("base", pkg_cfg)
    assert_raises(UserWarning, lambda: add_option('base', pkg_cfg))


def test_manage_update_opt_raise_error_if_not_already_installed():
    pkg_cfg = dict(default_cfg)
    assert_raises(UserWarning, lambda: update_option('base', pkg_cfg))


def test_manage_update_same_opt_do_not_change_anything():
    pkg_cfg = dict(default_cfg)
    pkg_cfg = add_option('base', pkg_cfg)
    pkg_cfg['base']['owner'] = "custom"

    mem = dict(pkg_cfg['base'])
    pkg_cfg = update_option('base', pkg_cfg)
    assert mem == pkg_cfg['base']


def test_manage_edit_opt_raise_error_if_not_already_installed():
    pkg_cfg = {}
    assert_raises(UserWarning, lambda: edit_option('base', pkg_cfg))
