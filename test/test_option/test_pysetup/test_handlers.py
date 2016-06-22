from copy import deepcopy

from pkglts.config_managment import pkg_env


def test_pkg_url_empty_default():
    env = pkg_env(dict(pysetup={"intended_versions": ["27"]}))
    assert env.globals['pysetup'].pkg_url == ""


def test_pkg_url_look_multiple_places():
    cfg = dict(base={'pkgname': 'toto', 'namespace': 'oa', 'url': None},
               github={'url': None},
               pypi={'classifiers': [], 'url': None},
               readthedocs={'project': 'project'},
               pysetup={'intended_versions': ["27"]})

    for name in ("base", "github", "pypi", "readthedocs"):
        loc_cfg = deepcopy(cfg)
        loc_cfg[name]['url'] = name
        env = pkg_env(loc_cfg)
        assert env.globals['pysetup'].pkg_url == name


def test_requirements():
    cfg = dict(test={},
               pysetup={'intended_versions': ["27"]})
    env = pkg_env(cfg)
    assert len(env.globals['pysetup'].requirements('install')) == 0
    assert len(env.globals['pysetup'].requirements('dvlpt')) == 2

