from copy import deepcopy

from pkglts.config_management import Config


def test_pkg_url_empty_default():
    cfg = Config(dict(pysetup={"intended_versions": ["2.7"]}))
    cfg.load_extra()
    assert cfg._env.globals['pysetup'].pkg_url == ""


def test_pkg_url_look_multiple_places():
    tpl_cfg = dict(base={'pkgname': 'toto', 'namespace': 'oa', 'url': None},
                   doc={'fmt': 'rst'},
                   github={'url': None, 'project': 'project', 'owner': 'toto'},
                   gitlab={'url': None, 'project': 'project', 'owner': 'toto'},
                   pypi={'classifiers': [], 'servers': [dict(name="pypi", url="https://upload.pypi.org/legacy/")]},
                   readthedocs={'project': 'project'},
                   pysetup={'intended_versions': ["2.7"]})

    for name in ("base", "github", "gitlab"):  # TODO, "pypi", "readthedocs"):
        loc_cfg = deepcopy(tpl_cfg)
        loc_cfg[name]['url'] = name
        cfg = Config(loc_cfg)
        cfg.load_extra()
        assert cfg._env.globals['pysetup'].pkg_url == name


def test_py_min_ver_uses_min_intended_version():
    cfg = Config(dict(pysetup={"intended_versions": ["2.7"]}))
    cfg.load_extra()
    assert cfg._env.globals['pysetup'].py_min_ver == "2.7"

    cfg = Config(dict(pysetup={"intended_versions": ["2.7", "3.6"]}))
    cfg.load_extra()
    assert cfg._env.globals['pysetup'].py_min_ver == "2.7"

    cfg = Config(dict(pysetup={"intended_versions": ["3.6", "3.7"]}))
    cfg.load_extra()
    assert cfg._env.globals['pysetup'].py_min_ver == "3.6"

    cfg = Config(dict(pysetup={"intended_versions": ["3.9", "3.10"]}))
    cfg.load_extra()
    assert cfg._env.globals['pysetup'].py_min_ver == "3.9"
