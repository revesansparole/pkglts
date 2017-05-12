from glob import glob
from importlib import import_module
from os import path

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
    # walk through all possible options
    option_basedir = path.join(path.dirname(get_data_dir()), 'pkglts', 'option')
    for pth in glob("{}/*/".format(option_basedir)):
        option_name = path.basename(path.dirname(pth))
        if not option_name.startswith("_"):
            # check 'require' module exists for each option
            try:
                opt_req = import_module("pkglts.option.%s.require" % option_name)
                assert len(getattr(opt_req, 'option')) >= 0
                assert len(getattr(opt_req, 'setup')) >= 0
                assert len(getattr(opt_req, 'install')) >= 0
                assert len(getattr(opt_req, 'dvlpt')) >= 0
            except ImportError:
                assert False


