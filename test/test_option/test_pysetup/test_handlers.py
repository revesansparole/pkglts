from copy import deepcopy

from pkglts.config_management import Config


def test_pkg_url_empty_default():
    cfg = Config(dict(pysetup={"intended_versions": ["27"],
                               'require': []}))
    cfg.load_extra()
    assert cfg._env.globals['pysetup'].pkg_url == ""


def test_pkg_url_look_multiple_places():
    tpl_cfg = dict(base={'pkgname': 'toto', 'namespace': 'oa', 'url': None},
                   doc={'fmt': 'rst'},
                   github={'url': None, 'project': 'project', 'owner': 'toto'},
                   gitlab={'project_url': None, 'project': 'project', 'owner': 'toto'},
                   pypi={'classifiers': [], 'url': None},
                   readthedocs={'project': 'project'},
                   pysetup={'intended_versions': ["27"],
                            'require': []})
    
    for name in ("base", "github", "gitlab", "pypi", "readthedocs"):
        loc_cfg = deepcopy(tpl_cfg)
        if name == "gitlab":
            loc_cfg[name]['project_url'] = name
        else:
            loc_cfg[name]['url'] = name
        cfg = Config(loc_cfg)
        cfg.load_extra()
        assert cfg._env.globals['pysetup'].pkg_url == name


def test_requirements():
    cfg = Config(dict(test={'suite_name': 'pytest'},
                      pysetup={'intended_versions': ["27"],
                               'require': []}))
    cfg.load_extra()
    assert len(cfg._env.globals['pysetup'].requirements('install')) == 0
    assert len(cfg._env.globals['pysetup'].requirements('dvlpt')) == 2
