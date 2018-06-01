from pkglts.config_management import Config


def test_exclude_lines_no_empty():
    exclude_lines = ['a', 'b']
    cfg = Config(dict(coverage={'exclude_lines': exclude_lines}))
    cfg.load_extra()
    assert cfg._env.globals['coverage'].exclude_lines == exclude_lines


def test_exclude_lines_empty():
    cfg = Config(dict(coverage={}))
    cfg.load_extra()
    assert cfg._env.globals['coverage'].exclude_lines == []
