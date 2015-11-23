from argparse import ArgumentParser, RawTextHelpFormatter
import logging

# from .local import installed_options
from .manage import (clean, get_pkg_config,
                     init_pkg, install_example_files,
                     regenerate,
                     add_option, edit_option,
                     # update_option, update_pkg,
                     write_pkg_config)


logger = logging.getLogger(__name__)


def action_clean(*args, **kwds):
    """ Clean package of all un necessary files.
    """
    del args  # unused
    del kwds  # unused
    logger.info("clean package")
    clean()


def action_init(*args, **kwds):
    """ Initialize environment for use of pkglts.
    """
    del args  # unused
    del kwds  # unused
    logger.info("init package")
    init_pkg()


def action_clear(*args, **kwds):
    """ Attempt to free the package from pkglts interactions.
    """
    del args  # unused
    del kwds  # unused
    logger.info("clear")
    print("TODO")


def action_update(*args, **kwds):
    """ Check if a new version of pkglts is available.
    """
    del args  # unused
    del kwds  # unused
    logger.info("update")
    print("TODO")


def action_regenerate(*args, **kwds):
    """ Regenerate all files in the package.
    """
    del args  # unused
    overwrite = 'overwrite' in kwds

    logger.info("regenerate")

    pkg_cfg = get_pkg_config()
    clean()
    regenerate(pkg_cfg, overwrite=overwrite)
    write_pkg_config(pkg_cfg)


def action_add(*args, **kwds):
    """ Add new options in the package.
    """
    del kwds  # unused
    if len(args) == 0:
        raise UserWarning("need to specify at least one option name")

    logger.info("add option")
    pkg_cfg = get_pkg_config()
    for name in args:
        pkg_cfg = add_option(name, pkg_cfg)

    write_pkg_config(pkg_cfg)


def action_remove(*args, **kwds):
    """ Remove options from the package.
    """
    del kwds  # unused
    if len(args) == 0:
        raise UserWarning("need to specify at least one option name")

    logger.info("remove option")
    print("TODO")


def action_edit(*args, **kwds):
    """ Edit options already in the package.
    """
    del kwds  # unused
    if len(args) == 0:
        raise UserWarning("need to specify at least one option name")

    pkg_cfg = get_pkg_config()
    for name in args:
        pkg_cfg = edit_option(name, pkg_cfg)

    write_pkg_config(pkg_cfg)


def action_example(*args, **kwds):
    """ Install example files associated with options.
    """
    del kwds  # unused
    if len(args) == 0:
        raise UserWarning("need to specify at least one option name")

    logger.info("install examples")
    pkg_cfg = get_pkg_config()
    for name in args:
        install_example_files(name, pkg_cfg)


action = dict(clean=action_clean,
              init=action_init,
              clear=action_clear,
              update=action_update,
              regenerate=action_regenerate,
              rg=action_regenerate,
              add=action_add,
              remove=action_remove,
              edit=action_edit,
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
