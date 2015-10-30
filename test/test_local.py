from nose.tools import assert_raises

from pkglts.local import (load_handlers, load_all_handlers,
                          installed_options, src_dir)


print(__file__)


def test_src_dir():
    pkg_cfg = {}
    assert_raises(KeyError, lambda: src_dir(pkg_cfg))

    pkg_cfg['base'] = {}
    assert_raises(KeyError, lambda: src_dir(pkg_cfg))

    pkg_cfg['base']['pkgname'] = 'toto'
    assert_raises(KeyError, lambda: src_dir(pkg_cfg))

    pkg_cfg['base']['namespace'] = None
    dir1 = src_dir(pkg_cfg)
    pkg_cfg['base']['namespace'] = 'oa'
    dir2 = src_dir(pkg_cfg)

    assert dir1 != dir2


def test_installed_options_handle_hash_key():
    cfg = {'toto': {}, 'titi': None}
    assert set(installed_options(cfg)) == {'toto', 'titi'}

    cfg['hash'] = {}
    assert set(installed_options(cfg)) == {'toto', 'titi'}


def test_load_handlers_fail_if_unknown_option():
    assert_raises(KeyError, lambda: load_handlers('toto'))


def test_load_handlers_load_functions_in_config_handlers():
    h = load_handlers('base')
    assert 'base' in h
    assert 'upper' in h


def test_load_all_handlers():
    pkg_cfg = {'base': {}, 'doc': {}}
    h = load_all_handlers(pkg_cfg)
    assert 'base' in h
    assert 'doc' in h
