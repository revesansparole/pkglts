from argparse import ArgumentParser
from glob import glob
from os import path

import pkglts
from pkglts.config_management import Config
from pkglts.option.doc.option import OptionDoc
from pkglts.option.sphinx.option import OptionSphinx
from pkglts.option.test.option import OptionTest
from pkglts.option_tools import available_options
from pkglts.small_tools import is_valid_identifier


def pkglts_opts():
    # walk through all possible options defined by pkglts
    option_basedir = path.join(path.dirname(pkglts.__file__), 'option')
    for pth in glob("{}/*/".format(option_basedir)):
        option_name = path.basename(path.dirname(pth))
        if not option_name.startswith("_"):
            try:
                yield available_options[option_name]
            except KeyError:
                assert False


def test_version_is_defined():
    for opt in pkglts_opts():
        assert opt.version() != "0.0.0"


def test_root_dir_is_defined():
    for opt in pkglts_opts():
        assert opt.root_dir() is not None


def test_options_expose_parameters():
    for opt in pkglts_opts():
        cfg = {}
        opt.update_parameters(cfg)
        assert len(cfg) == 1


def test_require_correctly_defined():
    cfg = Config(dict(base={}))
    OptionDoc('doc').update_parameters(cfg)
    OptionTest('test').update_parameters(cfg)
    OptionSphinx('sphinx').update_parameters(cfg)

    for opt in pkglts_opts():
        assert len(tuple(opt.require_option())) >= 0
        assert len(tuple(opt.require(cfg))) >= 0


def test_tools_correctly_defined():
    cfg = Config(dict(base={}))

    parser = ArgumentParser(description='Package structure manager')
    subparsers = parser.add_subparsers(dest='subcmd', help='sub-command help')

    for opt in pkglts_opts():
        for tool in opt.tools(cfg):
            name, action = tool(subparsers)
            assert is_valid_identifier(name)
            assert callable(action)
