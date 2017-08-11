from glob import glob
from os import path

from pkglts.config_management import Config
from pkglts.data_access import get_data_dir
from pkglts.option_tools import available_options


def test_options_expose_parameters():
    # walk through all possible options defined by pkglts
    option_basedir = path.join(path.dirname(get_data_dir()), 'pkglts', 'option')
    for pth in glob("{}/*/".format(option_basedir)):
        option_name = path.basename(path.dirname(pth))
        if not option_name.startswith("_"):
            # check 'update_parameters' exists for each option
            try:
                opt = available_options[option_name]
                cfg = {}
                opt.update_parameters(cfg)
                assert len(cfg) == 1
            except KeyError:
                assert False


def test_require_correctly_defined():
    cfg = Config(dict(base={}, doc={'fmt': 'rst'}, test={'suite_name': 'pytest'}))

    # walk through all possible options
    option_basedir = path.join(path.dirname(get_data_dir()), 'pkglts', 'option')
    for pth in glob("{}/*/".format(option_basedir)):
        option_name = path.basename(path.dirname(pth))
        if not option_name.startswith("_"):
            # check 'require' function exists for each option
            try:
                opt = available_options[option_name]
                assert len(opt.require('option', cfg)) >= 0
                assert len(opt.require('setup', cfg)) >= 0
                assert len(opt.require('install', cfg)) >= 0
                assert len(opt.require('dvlpt', cfg)) >= 0
            except ImportError:
                assert False
