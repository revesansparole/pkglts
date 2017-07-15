from pkglts.config_management import Config


def test_badge():
    cfg = Config(dict(base={'pkgname': "pkg", 'namespace': None,
                            "url": "http://toto"},
                      pysetup={"intended_versions": ["27", "28"],
                               'require': []},
                      pypi={'classifiers': []}))
    cfg.load_extra()
    assert ".. image:" in cfg._env.globals['pypi'].badge


def test_auto_classifiers():
    cfg = Config(dict(base={'pkgname': "pkg", 'namespace': None,
                            "url": "http://toto"},
                      pysetup={"intended_versions": ["27", "28"],
                               'require': []},
                      pypi={'classifiers': []}))
    cfg.load_extra()
    section = cfg._env.globals['pypi']
    assert "Programming Language :: Python" in section.auto_classifiers
    assert "Programming Language :: Python :: 2.7" in section.auto_classifiers
