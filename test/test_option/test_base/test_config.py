from pkglts.config_management import create_env
from pkglts.option.base.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 5


def test_config_check_pkg_names():
    for pkg in ('1mypkg', ' mypkg', '1', '1.mypkg',
                ' .mypkg', '.mypkg', 'None.mypkg', 'oa.o.mypkg'):
        env = create_env(dict(base={'pkgname': pkg,
                                    'namespace': None,
                                    'namespace_method': "pkg_util",
                                    'owner': 'moi',
                                    'url': None}))
        assert 'pkgname' in check(env)
        env = create_env(dict(base={'pkgname': 'toto',
                                    'namespace': pkg,
                                    'namespace_method': "pkg_util",
                                    'owner': 'moi',
                                    'url': None}))
        assert 'namespace' in check(env)

    env = create_env(dict(base={'pkgname': 'toto',
                                'namespace': None,
                                'namespace_method': "toto",
                                'owner': 'moi',
                                'url': None}))
    assert 'namespace_method' in check(env)


def test_require():
    cfg = dict(base={})
    env = create_env(cfg)

    assert len(require('option', env)) == 0
    assert len(require('setup', env)) == 0
    assert len(require('install', env)) == 0
    assert len(require('dvlpt', env)) == 0
