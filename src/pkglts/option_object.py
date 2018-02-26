"""
Base class for options.
"""
from os.path import dirname, exists, join as pj


class Option(object):
    """Base class to store information associated with an option
    """

    def __init__(self, name):
        self._name = name

    def root_dir(self):
        """Base directory containing option definition files.

        Returns:
            (str|Path)
        """
        return dirname(__file__)

    def example_dir(self):
        """Directory containing option example files.

        Returns:
            (str|Path)
        """
        pth = pj(self.root_dir(), 'example')
        if exists(pth):
            return pth

        return None

    def resource_dir(self):
        """Directory containing option resource files.

        Returns:
            (str|Path)
        """
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
        cfg[self._name] = {}

        return cfg

    def check(self, cfg):
        """Check validity of parameters for this option.

        Args:
            cfg (Config):  current package configuration

        Returns:
            (list of str): list of failing params
        """
        return []

    def require(self, purpose, cfg):
        """Check dependencies for this option.

        Args:
            purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
            cfg (Config):  current package configuration

        Returns:
            (list of Dependency): list of modules or options this option require
        """
        return []

    def environment_extensions(self, cfg):
        """Get jinja2 environment extensions defined by this option.

        Args:
            cfg (Config):  current package configuration

        Returns:
            (dict of str: any): extensions defined by this option
        """
        return {}

    def regenerate(self, *args, **kwds):
        """Call regenerate associated with this option.

        Returns:
            (any)
        """
        return None

    def tools(self, cfg):
        """Iterate on tools defined by this option.

        Args:
            cfg (Config):  current package configuration

        Returns:
            (iter of func): cli parser
        """
        return []
