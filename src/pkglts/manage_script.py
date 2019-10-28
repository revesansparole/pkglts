"""
Define actions that can be called with the CLI.
"""
import json
import logging
from argparse import ArgumentParser

from . import logging_tools
from .config_management import get_pkg_config, write_pkg_config
from .manage import add_option, clean, init_pkg, install_example_files, regenerate_option, regenerate_package
from .option_tools import available_options
from .version_management import outdated_options, write_pkg_version

LOGGER = logging.getLogger(__name__)


def action_info(cfg, **kwds):
    """Display info on package for debug purpose.
    """
    LOGGER.info("package info")
    print("current config (after resolution)")
    opt_names = kwds['option']
    all_opts = False
    if not opt_names:
        opt_names = cfg.installed_options(return_sorted=True)
        all_opts = True

    outdated = outdated_options(cfg)

    for name in opt_names:
        if name in outdated:
            print("%s: OUTDATED" % name)
        else:
            print(name)
        print(json.dumps(cfg[name], sort_keys=True, indent=2))

    if all_opts:
        print("other available options:")
        for opt_name in sorted(set(available_options) - set(cfg.installed_options())):
            print("  ", opt_name)


def action_clean(cfg, **kwds):
    """Clean package of all un necessary files.
    """
    del cfg, kwds  # unused
    LOGGER.info("clean package")
    clean()


def action_init(cfg, **kwds):
    """Initialize environment for use of pkglts.
    """
    if cfg is not None:
        LOGGER.warning("Directory is already a pkglts package")
        return

    init_pkg()

    if kwds:
        action_add(get_pkg_config(), **kwds)


def action_clear(cfg, **kwds):
    """Attempt to free the package from pkglts interactions.
    """
    del cfg, kwds  # unused
    LOGGER.info("clear")
    print("TODO")


def action_update(cfg, **kwds):
    """Check if a new version of pkglts is available.
    """
    del cfg, kwds  # unused
    LOGGER.info("update")
    print("TODO")


def action_regenerate(cfg, **kwds):
    """Regenerate all files in the package.
    """
    outdated = outdated_options(cfg)
    if len(outdated) > 0:
        out_fmt = "\n".join(outdated)
        LOGGER.warning("Some options are outdated,"
                       " please upgrade pkglts and/or all the following options:\n"
                       "%s" % out_fmt)
        return

    clean()

    if kwds['option']:
        for name in kwds['option']:
            LOGGER.info("regenerate '%s'", name)
            regenerate_option(cfg, name, overwrite=kwds['overwrite'])
    else:
        LOGGER.info("regenerate package")
        regenerate_package(cfg, overwrite=kwds['overwrite'])

    write_pkg_version(cfg)


def action_add(cfg, **kwds):
    """Add new options in the package.
    """
    LOGGER.info("add option")
    for name in kwds['option']:
        cfg = add_option(name, cfg)

    write_pkg_config(cfg)


def action_remove(cfg, **kwds):
    """Remove options from the package.
    """
    del cfg, kwds
    LOGGER.info("remove option")
    print("TODO")


def action_example(cfg, **kwds):
    """Install example files associated with options.
    """
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
        rg=action_regenerate,
        add=action_add,
        remove=action_remove,
        example=action_example
    )
    # parse argument line
    parser = ArgumentParser(description='Package structure manager')
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="increase output verbosity")

    subparsers = parser.add_subparsers(dest='subcmd', help='sub-command help')

    parser_info = subparsers.add_parser('info', help=action_info.__doc__)
    parser_info.add_argument('option', nargs='*',
                             help="name of option to fetch info")

    parser_clean = subparsers.add_parser('clean', help=action_clean.__doc__)

    parser_init = subparsers.add_parser('init', help=action_init.__doc__)
    parser_init.add_argument('option', nargs='*',
                             help="name of option to add during init")
    parser_clear = subparsers.add_parser('clear', help=action_clear.__doc__)
    parser_update = subparsers.add_parser('update', help=action_update.__doc__)
    parser_rg = subparsers.add_parser('rg', help=action_regenerate.__doc__)
    parser_rg.add_argument('option', nargs='*',
                           help="name of option to add")
    parser_rg.add_argument("--overwrite", action='store_true',
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

    # try to read package config for extra commands
    try:
        cfg = get_pkg_config()
    except IOError:
        cfg = None
    else:
        # add option commands
        for opt_name in cfg.installed_options():
            for parser_tool in available_options[opt_name].tools(cfg):
                name, action_tool = parser_tool(subparsers)
                action[name] = action_tool

    kwds = vars(parser.parse_args())
    logging_tools.main(kwds.pop('verbosity'))

    # perform action
    subcmd = kwds.pop('subcmd')
    if cfg is None and subcmd != "init":
        LOGGER.error("Directory is not a pkglts package, run pmg init first")
        return

    action[subcmd](cfg, **kwds)


if __name__ == '__main__':
    main()
