"""
This tool will try to bump the version number of the package.
"""
import logging

import semver
from pkglts.config_management import write_pkg_config

LOGGER = logging.getLogger(__name__)


def action_bump(cfg, **kwds):
    """Bump version number.
    """
    LOGGER.info("Bump version")
    pos = kwds['pos']
    # update both the actual config and its associated template
    for sec in (cfg['version'], cfg.template()['version']):
        if pos == 'major':
            sec['major'] += 1
            sec['minor'] = 0
            sec['post'] = 0
        elif pos == 'minor':
            sec['minor'] += 1
            sec['post'] = 0
        elif pos == 'post':
            sec['post'] += 1
        else:
            try:
                version = semver.parse(pos)
                sec['major'] = version['major']
                sec['minor'] = version['minor']
                sec['post'] = version['patch']
            except ValueError:
                LOGGER.error("Bump version: invalid argument '%s'", pos)

    write_pkg_config(cfg)


def parser_bump(subparsers):
    """Associate a CLI to this tool.

    Notes: The CLI will be a subcommand of pmg.

    Args:
        subparsers (ArgumentParser): entity to create a subparsers

    Returns:
        (string): a unique id for this parser
        (callable): the action to perform
    """
    parser = subparsers.add_parser('bump', help=action_bump.__doc__)
    parser.add_argument('pos', help="Element of version to bump {major, minor, post or X.X.X}")

    return 'bump', action_bump
