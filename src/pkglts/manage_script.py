from argparse import ArgumentParser, RawTextHelpFormatter
import logging

from .config_management import (get_pkg_config, write_pkg_config)
from .manage import (clean, init_pkg, install_example_files,
                     regenerate_package, regenerate_option, add_option)
from .tool.history import action_history

logger = logging.getLogger(__name__)


def action_info(*args, **kwds):
    """Display info on package for debug purpose.
    """
    del args  # unused
    del kwds  # unused
    logger.info("package info")
    from pkglts.option_tools import available_options
    print("available_options:")
    for opt_name in available_options:
        print("  ", opt_name)
    from pkglts.config_management import get_pkg_config
    cfg = get_pkg_config()
    print("current config (after resolution)")
    for opt_name, opt_params in cfg.items():
        print(opt_name, opt_params)


def action_clean(*args, **kwds):
    """Clean package of all un necessary files.
    """
    del args  # unused
    del kwds  # unused
    logger.info("clean package")
    clean()


def action_init(*args, **kwds):
    """Initialize environment for use of pkglts.
    """
    init_pkg()

    if len(args) > 0:
        action_add(*args, **kwds)


def action_clear(*args, **kwds):
    """Attempt to free the package from pkglts interactions.
    """
    del args  # unused
    del kwds  # unused
    logger.info("clear")
    print("TODO")


def action_update(*args, **kwds):
    """Check if a new version of pkglts is available.
    """
    del args  # unused
    del kwds  # unused
    logger.info("update")
    print("TODO")


def action_regenerate(*args, **kwds):
    """Regenerate all files in the package.
    """
    overwrite = 'overwrite' in kwds

    cfg = get_pkg_config()
    clean()

    if len(args) == 0:
        logger.info("regenerate package")
        regenerate_package(cfg, overwrite=overwrite)
    else:
        for name in args:
            logger.info("regenerate '%s'" % name)
            regenerate_option(cfg, name, overwrite=overwrite)


def action_add(*args, **kwds):
    """Add new options in the package.
    """
    del kwds  # unused
    if len(args) == 0:
        raise UserWarning("need to specify at least one option name")

    logger.info("add option")
    cfg = get_pkg_config()
    for name in args:
        cfg = add_option(name, cfg)

    write_pkg_config(cfg)


def action_remove(*args, **kwds):
    """Remove options from the package.
    """
    del kwds  # unused
    if len(args) == 0:
        raise UserWarning("need to specify at least one option name")

    logger.info("remove option")
    print("TODO")


def action_example(*args, **kwds):
    """Install example files associated with options.
    """
    del kwds  # unused
    if len(args) == 0:
        raise UserWarning("need to specify at least one option name")

    logger.info("install examples")
    cfg = get_pkg_config()
    for name in args:
        install_example_files(name, cfg)


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


def main():
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

    args = parser.parse_args()
    if args.extra is None:
        extra = {}
    else:
        extra = dict(args.extra)

    # perform action
    action[args.action](*args.action_args, **extra)


if __name__ == '__main__':
    main()
