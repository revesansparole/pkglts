from argparse import ArgumentParser, RawTextHelpFormatter
import logging

from .config_managment import (get_pkg_config, installed_options,
                               write_pkg_config)
from .manage import (clean, init_pkg, install_example_files,
                     regenerate_package, regenerate_option, add_option)


logger = logging.getLogger(__name__)


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
    del args  # unused
    del kwds  # unused
    init_pkg()


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

    env = get_pkg_config()
    clean()

    if len(args) == 0:
        logger.info("regenerate package")
        regenerate_package(env, overwrite=overwrite)
    else:
        name = [args[0]]
        logger.info("regenerate '%s'" % name)
        regenerate_option(env, name, overwrite=overwrite)


def action_add(*args, **kwds):
    """Add new options in the package.
    """
    del kwds  # unused
    if len(args) == 0:
        raise UserWarning("need to specify at least one option name")

    logger.info("add option")
    env = get_pkg_config()
    for name in args:
        env = add_option(name, env)

    write_pkg_config(env)


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
    env = get_pkg_config()
    for name in args:
        install_example_files(name, env)


action = dict(clean=action_clean,
              init=action_init,
              clear=action_clear,
              update=action_update,
              regenerate=action_regenerate,
              rg=action_regenerate,
              add=action_add,
              remove=action_remove,
              example=action_example)


def main():
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

    action[args.action](*args.action_args, **extra)


if __name__ == '__main__':
    main()
