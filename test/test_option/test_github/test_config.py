from pkglts.option.github.config import check, parameters


def test_parameters():
    assert len(parameters) == 1


def test_config_check_project_exists():
    pkg_cfg = dict(github={'project': ""})
    assert 'project' in check(pkg_cfg)
