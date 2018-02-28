"""
Dependency object to handle multi dependency managers.
"""
import logging

LOGGER = logging.getLogger(__name__)


class Dependency(object):
    """Simple container to keep track of all the required
    info to install a dependency.
    """

    def __init__(self, name, version=None, pkg_mng=None, channel=None):
        self.name = name
        """name of dependency"""

        self.version = version
        """expected version"""

        self.package_manager = pkg_mng
        """either conda, pip or git url"""

        self.channel = channel
        """place to find the dependency depends on package_manager"""

    def __str__(self):
        return "dep: {}".format(self.name)

    def _conda_fmt_name(self):
        if self.version is None:
            version = ""
        else:
            version = self.version
            if version[:2] in ('==', '>=', '<=', "~="):
                LOGGER.warning("bad version specification for '%s' with conda, use '=' by default", self.name)
                version = "=" + version[2:]
            elif version[0] != '=':
                version = "=" + version
        return "{}{}".format(self.name, version)

    def _pip_fmt_name(self):
        if self.version is None:
            version = ""
        else:
            version = self.version
            if version[:2] not in ('==', '>=', '<=', "~="):
                if len(version.split(".")) < 3:
                    version = ">=" + version
                else:
                    version = "==" + version
        return "{}{}".format(self.name, version)

    def conda_full_name(self):
        """Produce fully qualified name with version number.

        Returns:
            (str)
        """
        return self._conda_fmt_name()

    def pip_full_name(self):
        """Produce fully qualified name with version number.

        Returns:
            (str)
        """
        if self.is_pip(strict=False):
            return self._pip_fmt_name()

        if self.is_conda(strict=True):
            return self._conda_fmt_name()

        # TODO assume valid git url
        return "walou {}".format(self.name)

    def is_conda(self, strict=True):
        """Check whether this dependency can be managed by conda

        Args:
            strict (bool): whether only conda can manage this dep

        Returns:
            (bool)
        """
        if strict:
            return self.package_manager == 'conda'

        return self.package_manager is None or self.package_manager == 'conda'

    def is_pip(self, strict=True):
        """Check whether this dependency can be managed by pip

        Args:
            strict (bool): whether only pip can manage this dep

        Returns:
            (bool)
        """
        if strict:
            return self.package_manager == 'pip'

        return self.package_manager is None or self.package_manager == 'pip'

    def conda_install(self):
        """Produce command line needed to install this dependency.

        Returns:
            (str)
        """
        full_name = self.conda_full_name()

        if self.channel is None:
            return "conda install {}".format(full_name)

        return "conda install -c {} {}".format(self.channel, full_name)

    def pip_install(self):
        """Produce command line needed to install this dependency.

        Returns:
            (str)
        """
        full_name = self.pip_full_name()
        return "pip install {}".format(full_name)

    def fmt_conda_requirement(self):
        """Format dependency for conda requirements.yml files

        Returns:
            (str)
        """
        return self.conda_full_name()

    def fmt_pip_requirement(self, extended=False):
        """Format dependency for pip requirements.txt files

        Returns:
            (str)
        """
        txt = self._pip_fmt_name()
        if extended:
            if self.is_pip(strict=False):
                txt += "  # {}".format(self.pip_install())
            elif self.is_conda(strict=True):
                txt += "  # {}".format(self.conda_install())
            else:  # assume valid git url
                txt += "  # pip install git+{}".format(self.package_manager)

        return txt
