from glob import glob
from importlib import import_module
from os import path

from pkglts.config_management import create_env
from pkglts.data_access import get_data_dir


def test_config_contains_parameters():
    # walk through all possible options
    option_basedir = path.join(path.dirname(get_data_dir()), 'pkglts', 'option')
    for pth in glob("{}/*/".format(option_basedir)):
        option_name = path.basename(path.dirname(pth))
        if not option_name.startswith("_"):
            # check 'config' module exists for each option
            try:
                opt_cfg = import_module("pkglts.option.%s.config" % option_name)
                assert len(getattr(opt_cfg, 'parameters')) >= 0
            except ImportError:
                assert False


def test_handlers_exists():
    # walk through all possible options
    option_basedir = path.join(path.dirname(get_data_dir()), 'pkglts', 'option')
    for pth in glob("{}/*/".format(option_basedir)):
        option_name = path.basename(path.dirname(pth))
        if not option_name.startswith("_"):
            # check 'require' module exists for each option
            try:
                opt_hand = import_module("pkglts.option.%s.handlers" % option_name)
            except ImportError:
                assert False


def test_require_correctly_defined():
    cfg = dict(base={}, test={'suite_name': 'pytest'})
    env = create_env(cfg)

    # walk through all possible options
    option_basedir = path.join(path.dirname(get_data_dir()), 'pkglts', 'option')
    for pth in glob("{}/*/".format(option_basedir)):
        option_name = path.basename(path.dirname(pth))
        if not option_name.startswith("_"):
            # check 'require' function exists for each option
            try:
                opt_cfg = import_module("pkglts.option.%s.config" % option_name)
                assert len(opt_cfg.require('option', env)) >= 0
                assert len(opt_cfg.require('setup', env)) >= 0
                assert len(opt_cfg.require('install', env)) >= 0
                assert len(opt_cfg.require('dvlpt', env)) >= 0
            except ImportError:
                assert False


