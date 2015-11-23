from pkglts.option.doc.config import check, parameters


def test_parameters():
    assert len(parameters) == 2


def test_config_check_description_exists():
    pkg_cfg = dict(doc={'description': "", 'keywords': []})
    assert 'description' in check(pkg_cfg)
