import pytest
from pkglts.config_management import Config
from pkglts.option.plugin_project.option import OptionPluginProject


@pytest.fixture()
def opt():
    return OptionPluginProject('plugin_project')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['plugin_project']) == 1


def test_config_check_plugin_names(opt):
    cfg = Config(dict(plugin_project={'plugin_name': "walou"}))
    assert 'plugin_project.plugin_name' not in opt.check(cfg)

    for pkg in ('1mypkg', ' mypkg', '1', '1.mypkg',
                ' .mypkg', '.mypkg', 'None.mypkg', 'oa.o.mypkg'):
        cfg = Config(dict(plugin_project={'plugin_name': pkg}))
        assert 'plugin_project.plugin_name' in opt.check(cfg)


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(opt.require('option', cfg)) == 3
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 1
    assert len(opt.require('dvlpt', cfg)) == 0
