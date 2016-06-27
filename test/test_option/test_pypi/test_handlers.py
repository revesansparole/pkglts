from pkglts.config_managment import pkg_env


def test_badge():
    env = pkg_env(dict(base={'pkgname': "pkg", 'namespace': None,
                             "url": "http://toto"},
                       pysetup={"intended_versions": ["27", "28"]},
                       pypi={'classifiers': []}))
    assert ".. image:" in env.globals['pypi'].badge


def test_auto_classifiers():
    env = pkg_env(dict(base={'pkgname': "pkg", 'namespace': None,
                             "url": "http://toto"},
                       pysetup={"intended_versions": ["27", "28"]},
                       pypi={'classifiers': []}))
    assert "Programming Language :: Python" in env.globals['pypi'].auto_classifiers
    assert "Programming Language :: Python :: 2.7" in env.globals['pypi'].auto_classifiers
