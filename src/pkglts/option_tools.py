""" Some helpers for options
"""
import logging
from os.path import dirname, exists, join as pj

import pkg_resources

LOGGER = logging.getLogger(__name__)

available_options = {}
"""Dictionary of currently available option in pkglts. Discovered at run time"""

try:
    loc_input = raw_input
except NameError:
    loc_input = input


class Option(object):
    """Base class to store information associated with an option
    """

    def __init__(self):
        self._name = None
        self._root_dir = None
        self._update_parameters = None
        self._check = None
        self._require = None
        self._environment_extensions = None
        self._regenerate = None

    def from_entry_point(self, ept):
        """Associate an entry point with its correct attribute.

        Notes: does not load the entry point

        Args:
            ept (entry point): as returned by pkg_resources

        Returns:
            None
        """
        self._name, func_name = ept.name.split(".")
        if func_name == "root":
            self._root_dir = ept
        elif func_name == "update_parameters":
            self._update_parameters = ept
        elif func_name == "check":
            self._check = ept
        elif func_name == "require":
            self._require = ept
        elif func_name == "environment_extensions":
            self._environment_extensions = ept
        elif func_name == "regenerate":
            self._regenerate = ept
        else:
            # silently ignore other type of entry points
            LOGGER.error("unknown entry point attribute: '%s'", func_name)

    def root_dir(self):
        """Base directory containing option definition files."""
        if self._root_dir is None:
            raise UserWarning("Need to associate entry point first")

        if isinstance(self._root_dir, pkg_resources.EntryPoint):
            self._root_dir = dirname(self._root_dir.load().__file__)

        return self._root_dir

    def example_dir(self):
        """Directory containing option example files."""
        pth = pj(self.root_dir(), 'example')
        if exists(pth):
            return pth

        return None

    def resource_dir(self):
        """Directory containing option resource files."""
        pth = pj(self.root_dir(), 'resource')
        if exists(pth):
            return pth

        return None

    def update_parameters(self, cfg):
        """Update configuration with option parameters.

        Args:
            cfg (Config):  current package configuration

        Returns:
            (Config)
        """
        if self._update_parameters is None:
            cfg[self._name] = {}
            return

        if isinstance(self._update_parameters, pkg_resources.EntryPoint):
            self._update_parameters = self._update_parameters.load()

        return self._update_parameters(cfg)

    def check(self, *args, **kwds):
        """Check validity of parameters for this option.

        Returns:
            (list of str): list of failing params
        """
        if self._check is None:
            return []

        if isinstance(self._check, pkg_resources.EntryPoint):
            self._check = self._check.load()

        return self._check(*args, **kwds)

    def require(self, *args, **kwds):
        """Check dependencies for this option.

        Returns:
            (list of Dependency): list of modules or options this option require
        """
        if self._require is None:
            return []

        if isinstance(self._require, pkg_resources.EntryPoint):
            self._require = self._require.load()

        return self._require(*args, **kwds)

    def environment_extensions(self, *args, **kwds):
        """Get jinja2 environment extensions defined by this option.

        Returns:
            (list of func): extensions defined by this option
        """
        if self._environment_extensions is None:
            return {}

        if isinstance(self._environment_extensions, pkg_resources.EntryPoint):
            self._environment_extensions = self._environment_extensions.load()

        return self._environment_extensions(*args, **kwds)

    def regenerate(self, *args, **kwds):
        """Call regenerate associated with this option.

        Returns:
            (any)
        """
        if self._regenerate is None:
            return None

        if isinstance(self._regenerate, pkg_resources.EntryPoint):
            self._regenerate = self._regenerate.load()

        return self._regenerate(*args, **kwds)


def find_available_options():
    """Discover all available options.

    Returns:
        (list of Option)
    """
    for ept in pkg_resources.iter_entry_points(group='pkglts'):
        option_name = ept.name.split(".")[0]
        if option_name not in available_options:
            available_options[option_name] = Option()

        opt = available_options[option_name]
        opt.from_entry_point(ept)


def get_user_permission(action_name, default_true=True):
    """Helper function to input a yes or no question.

    Args:
        action_name (str): action to ask permission for.
        default_true (bool): whether answer is yes or no by default.

    Returns:
        (bool)
    """
    if default_true:
        ans = loc_input("%s [y], n?" % action_name) in ("", "y")
    else:
        ans = loc_input("%s y, [n]?" % action_name) == "y"

    return ans
