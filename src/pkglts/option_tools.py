""" Some helpers for options
"""

import logging
from importlib.metadata import EntryPoint, entry_points

LOGGER = logging.getLogger(__name__)


class EpDict(dict):
    """A simple dictionary to load EntryPoint at access time only"""

    def __getitem__(self, name):
        val = dict.__getitem__(self, name)
        if isinstance(val, EntryPoint):
            val = val.load()(name)
            self[name] = val

        return val

    def items(self):
        raise NotImplementedError("TODO is needed")

    def values(self):
        raise NotImplementedError("TODO is needed")


available_options = EpDict()
"""Dictionary of currently available option in pkglts. Discovered at run time"""


def find_available_options():
    """Discover all available options.

    Returns:
        (dict of str: Option)
    """
    for ept in entry_points(group="pkglts"):
        option_name = ept.name
        if option_name not in available_options:
            available_options[option_name] = ept


def get_user_permission(action_name, default_true=True):
    """Helper function to input a yes or no question.

    Args:
        action_name (str): action to ask permission for.
        default_true (bool): whether answer is yes or no by default.

    Returns:
        (bool)
    """
    if default_true:
        ans = input(f"{action_name} [y], n?") in ("", "y")
    else:
        ans = input(f"{action_name} y, [n]?") == "y"

    return ans
