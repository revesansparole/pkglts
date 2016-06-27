import json
import mock
from nose.tools import assert_raises, with_setup
from os import remove
from os.path import exists
from os.path import join as pj
from nose.tools import assert_raises

from pkglts.config_management import (create_env, current_pkg_cfg_version,
                                      default_cfg, get_pkg_config,
                                      installed_options, pkg_env,
                                      write_pkg_config)

from .small_tools import ensure_created, rmdir


tmp_dir = 'toto_mg_cfg'


def setup():
    ensure_created(tmp_dir)
    ensure_created(pj(tmp_dir, ".pkglts"))


def teardown():
    rmdir(tmp_dir)


def test_create_env():
    env = create_env(default_cfg)
    assert len(tuple(installed_options(env))) == 0

    cfg = dict(default_cfg)
    cfg['base'] = dict(a=1, b=2)
    env = create_env(cfg)
    assert len(tuple(installed_options(env))) == 1
    assert env.globals['base'].a == 1
    assert env.globals['base'].b == 2


def test_create_env_render_templates():
    cfg = dict(default_cfg)
    cfg['base'] = dict(a="a", b="b")
    cfg['tpl'] = dict(tpl1="{{ base.a }}",
                      tpl2="{{ base.b }} and {{ tpl.tpl1 }}")

    env = create_env(cfg)
    assert env.globals['tpl'].tpl1 == "a"
    assert env.globals['tpl'].tpl2 == "b and a"


def test_create_env_raise_error_if_unable_to_fully_render_templates():
    cfg = dict(default_cfg)

    cfg['base'] = dict(a="{{ base.b }}", b="{{ base.a }}")
    assert_raises(UserWarning, lambda: create_env(cfg))


def test_pkg_env_raise_error_if_option_not_defined():
    cfg = dict(default_cfg)
    cfg['babou'] = dict(a="a", b="b")

    assert_raises(KeyError, lambda: pkg_env(cfg))


def test_pkg_env_loads_specific_handlers_from_options():
    cfg = dict(default_cfg)
    cfg['base'] = dict(pkgname="toto", namespace="nm",
                       url=None, authors=[("moi", "moi@aussi")])

    env = pkg_env(cfg)
    assert hasattr(env.globals['base'], "pkg_full_name")


def test_get_pkg_config_read_cfg():
    cfg = dict(default_cfg)
    cfg['base'] = dict(pkgname="toto", namespace="nm",
                       url=None, authors=[("moi", "moi@aussi")])
    with open(pj(tmp_dir, ".pkglts/pkg_cfg.json"), 'w') as f:
        json.dump(cfg, f)

    env = get_pkg_config(tmp_dir)
    assert 'base' in env.globals


def test_get_pkg_config_handle_versions():
    cfg = dict(default_cfg)
    cfg["_pkglts"]["version"] = 0
    with open(pj(tmp_dir, ".pkglts/pkg_cfg.json"), 'w') as f:
        json.dump(cfg, f)

    env = get_pkg_config(tmp_dir)
    assert env.globals["_pkglts"].version == current_pkg_cfg_version


def test_pkg_cfg_read_write_maintains_templates():
    cfg = dict(default_cfg)
    cfg['base'] = dict(pkgname="toto", namespace="nm",
                       url=None, authors=[("moi", "moi@aussi")])
    cfg['license'] = dict(name="CeCILL-C", organization="org",
                          project="{{ base.pkgname }}", year="2015")

    with open(pj(tmp_dir, ".pkglts/pkg_cfg.json"), 'w') as f:
        json.dump(cfg, f)

    env = get_pkg_config(tmp_dir)
    assert env.globals['license'].project == "toto"

    write_pkg_config(env, tmp_dir)
    with open(pj(tmp_dir, ".pkglts/pkg_cfg.json"), 'r') as f:
        cfg = json.load(f)

    cfg["base"]["pkgname"] = "tutu"

    with open(pj(tmp_dir, ".pkglts/pkg_cfg.json"), 'w') as f:
        json.dump(cfg, f)

    env = get_pkg_config(tmp_dir)
    assert env.globals['license'].project == "tutu"
