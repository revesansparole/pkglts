import pytest
from pkglts.config_management import Config
from pkglts.option.plugin_project.option import OptionPluginProject


@pytest.fixture()
def opt():
    return OptionPluginProject('plugin_project')


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg['plugin_project']) == 1


def test_config_check_plugin_names(opt, cfg):
    cfg['plugin_project'] = {'plugin_name': "walou"}
    assert 'plugin_project.plugin_name' not in opt.check(cfg)

    for pkg in ('1mypkg', ' mypkg', '1', '1.mypkg',
                ' .mypkg', '.mypkg', 'None.mypkg', 'oa.o.mypkg'):
        cfg['plugin_project'] = {'plugin_name': pkg}
        assert 'plugin_project.plugin_name' in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 3


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 1
