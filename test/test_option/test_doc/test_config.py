from pkglts.config_management import create_env
from pkglts.option.doc.config import check, parameters


def test_parameters():
    assert len(parameters) == 2


def test_config_check_description_exists():
    env = create_env(dict(doc={'description': "mydescr", 'keywords': []}))
    assert env.globals['doc'].description == "mydescr"
    assert 'description' not in check(env)


def test_config_check_description_valid():
    env = create_env(dict(doc={'description': "", 'keywords': []}))
    assert 'description' in check(env)


def test_config_check_keywords_exists():
    env = create_env(dict(doc={'description': "mydescr", 'keywords': []}))
    assert len(env.globals['doc'].keywords) == 0
    assert 'keywords' not in check(env)
