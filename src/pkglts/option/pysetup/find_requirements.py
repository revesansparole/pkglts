"""
This tool will display all dependencies used by this package.
"""
import logging

LOGGER = logging.getLogger(__name__)


def action_find_reqs(cfg, **kwds):
    """Find dependencies used by this package.
    """
    LOGGER.info("Find requirements")
    print("TODO")


def parser_find_reqs(subparsers):
    """Associate a CLI to this tool.

    Notes: The CLI will be a subcommand of pmg.

    Args:
        subparsers (ArgumentParser): entity to create a subparsers

    Returns:
        (string): a unique id for this parser
        (callable): the action to perform
    """
    parser = subparsers.add_parser('reqs', help=action_find_reqs.__doc__)

    return 'reqs', action_find_reqs
