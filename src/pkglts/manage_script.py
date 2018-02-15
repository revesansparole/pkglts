"""
Define actions that can be called with the CLI.
"""
import json
import logging
from argparse import ArgumentParser, RawTextHelpFormatter

from . import logging_tools
from .config_management import get_pkg_config, write_pkg_config
from .manage import add_option, clean, init_pkg, install_example_files, regenerate_option, regenerate_package
from .tool.history import action_history

LOGGER = logging.getLogger(__name__)


def action_info(*args, **kwds):
    """Display info on package for debug purpose.
    """
    del args  # unused
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


def action_clean(*args, **kwds):
    """Clean package of all un necessary files.
    """
    del args  # unused
    del kwds  # unused
    LOGGER.info("clean package")
    clean()


def action_init(*args, **kwds):
    """Initialize environment for use of pkglts.
    """
    init_pkg()

    if args:
        action_add(*args, **kwds)


def action_clear(*args, **kwds):
    """Attempt to free the package from pkglts interactions.
    """
    del args  # unused
    del kwds  # unused
    LOGGER.info("clear")
    print("TODO")


def action_update(*args, **kwds):
    """Check if a new version of pkglts is available.
    """
    del args  # unused
    del kwds  # unused
    LOGGER.info("update")
    print("TODO")


def action_regenerate(*args, **kwds):
    """Regenerate all files in the package.
    """
    overwrite = 'overwrite' in kwds

    cfg = get_pkg_config()
    clean()

    if args:
        for name in args:
            LOGGER.info("regenerate '%s'", name)
            regenerate_option(cfg, name, overwrite=overwrite)
    else:
        LOGGER.info("regenerate package")
        regenerate_package(cfg, overwrite=overwrite)


def action_add(*args, **kwds):
    """Add new options in the package.
    """
    del kwds  # unused
    if not args:
        raise UserWarning("need to specify at least one option name")

    LOGGER.info("add option")
    cfg = get_pkg_config()
    for name in args:
        cfg = add_option(name, cfg)

    write_pkg_config(cfg)


def action_remove(*args, **kwds):
    """Remove options from the package.
    """
    del kwds  # unused
    if not args:
        raise UserWarning("need to specify at least one option name")

    LOGGER.info("remove option")
    print("TODO")


def action_example(*args, **kwds):
    """Install example files associated with options.
    """
    del kwds  # unused
    if not args:
        raise UserWarning("need to specify at least one option name")

    LOGGER.info("install examples")
    cfg = get_pkg_config()
    for name in args:
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
    parser = ArgumentParser(description='Package structure manager',
                            formatter_class=RawTextHelpFormatter)

    act_help = "type of action performed by pmg, one of:\n"
    for name, func in action.items():
        act_help += "\n  - %s: %s" % (name, func.__doc__)

    parser.add_argument('action', metavar='action',
                        choices=tuple(action.keys()),
                        help=act_help)

    parser.add_argument('action_args', nargs='*',
                        help="action to perform on the package")

    parser.add_argument('-e', metavar='extra', nargs=2, action='append',
                        help='extra arguments to pass to the action',
                        dest='extra')

    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="increase output verbosity")

    args = parser.parse_args()
    if args.extra is None:
        extra = {}
    else:
        extra = dict(args.extra)

    logging_tools.main(args.verbosity)

    # perform action
    action[args.action](*args.action_args, **extra)


if __name__ == '__main__':
    main()
