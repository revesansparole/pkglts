"""
Define actions that can be called with the CLI.
"""
import json
import logging
from argparse import ArgumentParser

from . import logging_tools
from .config_management import get_pkg_config, write_pkg_config
from .manage import add_option, clean, init_pkg, install_example_files, regenerate_option, regenerate_package
from .tool.history import action_history

LOGGER = logging.getLogger(__name__)


def action_info(**kwds):
    """Display info on package for debug purpose.
    """
    del kwds  # unused
    LOGGER.info("package info")
    from pkglts.option_tools import available_options
    print("available_options:")
    for opt_name in available_options:
        print("  ", opt_name)
    cfg = get_pkg_config()
    print("current config (after resolution)")
    for opt_name, opt_params in cfg.items():
        if not opt_name.startswith("_"):
            print(opt_name)
            print(json.dumps(opt_params, sort_keys=True, indent=2))


def action_clean(**kwds):
    """Clean package of all un necessary files.
    """
    del kwds  # unused
    LOGGER.info("clean package")
    clean()


def action_init(**kwds):
    """Initialize environment for use of pkglts.
    """
    init_pkg()

    if kwds:
        action_add(**kwds)


def action_clear(**kwds):
    """Attempt to free the package from pkglts interactions.
    """
    del kwds  # unused
    LOGGER.info("clear")
    print("TODO")


def action_update(**kwds):
    """Check if a new version of pkglts is available.
    """
    del kwds  # unused
    LOGGER.info("update")
    print("TODO")


def action_regenerate(**kwds):
    """Regenerate all files in the package.
    """
    cfg = get_pkg_config()
    clean()

    if kwds['option']:
        for name in kwds['option']:
            LOGGER.info("regenerate '%s'", name)
            regenerate_option(cfg, name, overwrite=kwds['overwrite'])
    else:
        LOGGER.info("regenerate package")
        regenerate_package(cfg, overwrite=kwds['overwrite'])


def action_add(**kwds):
    """Add new options in the package.
    """
    LOGGER.info("add option")
    cfg = get_pkg_config()
    for name in kwds['option']:
        cfg = add_option(name, cfg)

    write_pkg_config(cfg)


def action_remove(**kwds):
    """Remove options from the package.
    """
    LOGGER.info("remove option")
    print("TODO")
    del kwds


def action_example(**kwds):
    """Install example files associated with options.
    """
    LOGGER.info("install examples")
    cfg = get_pkg_config()
    for name in kwds['option']:
        install_example_files(name, cfg)


def main():
    """Run CLI evaluation"""
    action = dict(
        info=action_info,
        clean=action_clean,
        init=action_init,
        clear=action_clear,
        update=action_update,
        regenerate=action_regenerate,
        rg=action_regenerate,
        add=action_add,
        remove=action_remove,
        example=action_example,
        history=action_history
    )
    # parse argument line
    parser = ArgumentParser(description='Package structure manager')
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="increase output verbosity")

    subparsers = parser.add_subparsers(dest='subcmd', help='sub-command help')

    parser_info = subparsers.add_parser('info', help=action_info.__doc__)

    parser_clean = subparsers.add_parser('clean', help=action_clean.__doc__)

    parser_init = subparsers.add_parser('init', help=action_init.__doc__)
    parser_init.add_argument('option', nargs='*',
                             help="name of option to add during init")
    parser_clear = subparsers.add_parser('clear', help=action_clear.__doc__)
    parser_update = subparsers.add_parser('update', help=action_update.__doc__)
    parser_rg = subparsers.add_parser('rg', help=action_regenerate.__doc__)
    parser_rg.add_argument('option', nargs='*',
                           help="name of option to add")
    parser_rg.add_argument('--overwrite', type=bool, default=False,
                           help="Globally overwrite user modified files")

    parser_add = subparsers.add_parser('add', help=action_add.__doc__)
    parser_add.add_argument('option', nargs='+',
                            help="name of option to add")

    parser_remove = subparsers.add_parser('remove', help=action_remove.__doc__)
    parser_remove.add_argument('option', nargs='+',
                               help="name of option to remove")
    parser_example = subparsers.add_parser('example', help=action_example.__doc__)
    parser_example.add_argument('option', nargs='+',
                                help="name of option which offer example files")
    parser_history = subparsers.add_parser('history', help=action_history.__doc__)

    args = vars(parser.parse_args())

    logging_tools.main(args.pop('verbosity'))

    # perform action
    subcmd = args.pop('subcmd')
    action[subcmd](**args)


if __name__ == '__main__':
    main()
