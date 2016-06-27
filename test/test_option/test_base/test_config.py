from pkglts.config_management import create_env
from pkglts.option.base.config import check, parameters


def test_parameters():
    assert len(parameters) == 4


def test_config_check_pkg_names():
    for pkg in ('1mypkg', ' mypkg', '1', '1.mypkg',
                ' .mypkg', '.mypkg', 'None.mypkg', 'oa.o.mypkg'):
        env = create_env(dict(base={'pkgname': pkg,
                                    'namespace': None,
                                    'owner': 'moi',
                                    'url': None}))
        assert 'pkgname' in check(env)
        env = create_env(dict(base={'pkgname': 'toto',
                                    'namespace': pkg,
                                    'owner': 'moi',
                                    'url': None}))
        assert 'namespace' in check(env)
