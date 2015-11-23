from pkglts.option.version.config import check, parameters


def test_parameters():
    assert len(parameters) == 3


def test_config_check_version_numbers_are_valid():
    pkg_cfg = dict(version={'major': "", 'minor': "", 'post': ""})
    assert 'major' in check(pkg_cfg)
    assert 'minor' in check(pkg_cfg)
    assert 'post' in check(pkg_cfg)
    pkg_cfg = dict(version={'major': "a", 'minor': "a", 'post': "a"})
    assert 'major' in check(pkg_cfg)
    assert 'minor' in check(pkg_cfg)
    assert 'post' in check(pkg_cfg)
    pkg_cfg = dict(version={'major': "1", 'minor': "0", 'post': "2.dev"})
    assert 'post' in check(pkg_cfg)
