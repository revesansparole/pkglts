from pkglts.option.pysetup.config import check, parameters


def test_parameters():
    assert len(parameters) == 3


def test_config_check_author_name_exists():
    pkg_cfg = dict(pysetup={'author_name': "", 'author_email': "",
                            'intended_versions': ["27"]})
    assert 'author_name' in check(pkg_cfg)


def test_config_check_intended_version_exists():
    pkg_cfg = dict(pysetup={'author_name': "moi", 'author_email': "",
                            'intended_versions': []})
    assert 'intended_versions' in check(pkg_cfg)
