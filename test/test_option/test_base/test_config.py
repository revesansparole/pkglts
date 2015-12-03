from pkglts.option.base.config import check, parameters


def test_parameters():
    assert len(parameters) == 3


def test_config_check_pkg_names():
    for pkg in ('1mypkg', ' mypkg', '1', '1.mypkg',
                ' .mypkg', '.mypkg', 'None.mypkg', 'oa.o.mypkg'):
        pkg_cfg = dict(base={'pkgname': pkg,
                             'namespace': None,
                             'owner': 'moi'})
        assert 'pkgname' in check(pkg_cfg)
        pkg_cfg = dict(base={'pkgname': 'toto',
                             'namespace': pkg,
                             'owner': 'moi'})
        assert 'namespace' in check(pkg_cfg)
