from pkglts.config_management import Config


def test_url_auto_no_subgroup():
    cfg = Config(dict(gitlab={'owner': "moi", 'project': "project", 'server': "server", 'project_url': "Auto",
                              'sub_group': None}))
    cfg.load_extra()
    assert cfg._env.globals['gitlab'].url == "https://%s/%s/%s" % (cfg['gitlab']['server'], cfg['gitlab']['owner'],
                                                                   cfg['gitlab']['project'])


def test_url_auto_subgroup():
    cfg = Config(dict(gitlab={'owner': "moi", 'project': "project", 'server': "server", 'project_url': "Auto",
                              'sub_group': 'group'}))
    cfg.load_extra()
    assert cfg._env.globals['gitlab'].url == "https://%s/%s/%s/%s" % (cfg['gitlab']['server'], cfg['gitlab']['owner'],
                                                                      cfg['gitlab']['sub_group'],
                                                                      cfg['gitlab']['project'])


def test_url_not_auto():
    cfg = Config(dict(gitlab={'owner': "moi", 'project': "project", 'server': "server", 'project_url': "http://url",
                              'sub_group': 'group'}))
    cfg.load_extra()
    assert cfg._env.globals['gitlab'].url == cfg['gitlab']['project_url']
