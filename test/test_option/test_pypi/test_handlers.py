from pkglts.config_management import pkg_env


def test_badge():
    env = pkg_env(dict(base={'pkgname': "pkg", 'namespace': None,
                             "url": "http://toto"},
                       pysetup={"intended_versions": ["27", "28"],
                                'require': []},
                       pypi={'classifiers': []}))
    assert ".. image:" in env.globals['pypi'].badge


def test_auto_classifiers():
    env = pkg_env(dict(base={'pkgname': "pkg", 'namespace': None,
                             "url": "http://toto"},
                       pysetup={"intended_versions": ["27", "28"],
                                'require': []},
                       pypi={'classifiers': []}))
    section = env.globals['pypi']
    assert "Programming Language :: Python" in section.auto_classifiers
    assert "Programming Language :: Python :: 2.7" in section.auto_classifiers
