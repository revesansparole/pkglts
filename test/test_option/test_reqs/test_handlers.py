from pkglts.config_management import Config


def test_requirements():
    cfg = Config(dict(test={'suite_name': 'pytest'},
                      reqs={'require': []}))
    cfg.load_extra()
    assert len(cfg._env.globals['reqs'].requirements('install')) == 0
    assert len(cfg._env.globals['reqs'].requirements('test')) == 2
    assert len(cfg._env.globals['reqs'].intents()) >= 4
    assert len(cfg._env.globals['reqs'].conda_reqs('install')) >= 0
    assert len(cfg._env.globals['reqs'].pip_reqs('install')) >= 0
