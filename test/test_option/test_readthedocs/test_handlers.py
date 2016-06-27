from pkglts.config_managment import pkg_env


def test_badge():
    env = pkg_env(dict(readthedocs={'project': "project"}))
    assert ".. image:" in env.globals['readthedocs'].badge
