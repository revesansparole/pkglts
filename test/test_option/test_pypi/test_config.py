from pkglts.option.pypi.config import check, parameters


def test_parameters():
    assert len(parameters) == 1


def test_config_check_classifiers_exists():
    pkg_cfg = dict(pypi={'classifiers': []})
    assert 'classifiers' in check(pkg_cfg)
