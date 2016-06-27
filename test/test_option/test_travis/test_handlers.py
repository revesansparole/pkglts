from pkglts.config_managment import pkg_env


def test_badge():
    env = pkg_env(dict(travis={},
                       github={'owner': "moi", 'project': "project"}))
    assert ".. image:" in env.globals['travis'].badge
