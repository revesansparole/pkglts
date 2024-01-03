from pkglts.config_management import Config


def test_badge():
    cfg = Config(dict(base={'pkgname': "pkg", 'namespace': None,
                            "url": "http://toto"},
                      doc={'fmt': 'rst'},
                      pyproject={"intended_versions": ["2.7", "2.8"],
                               'require': []},
                      pypi={'classifiers': [], 'servers': [dict(name="pypi", url="https://upload.pypi.org/legacy/")]}))
    cfg.load_extra()
    assert "pypi" in cfg._env.globals['pypi'].badge.name


def test_auto_classifiers():
    cfg = Config(dict(base={'pkgname': "pkg", 'namespace': None,
                            "url": "http://toto"},
                      doc={'fmt': 'rst'},
                      pyproject={"intended_versions": ["2.7", "2.8"],
                               'require': []},
                      pypi={'classifiers': [], 'servers': []}))
    cfg.load_extra()
    section = cfg._env.globals['pypi']
    assert "Programming Language :: Python" in section.auto_classifiers
    assert "Programming Language :: Python :: 2.7" in section.auto_classifiers
