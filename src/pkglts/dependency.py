import logging

logger = logging.getLogger(__name__)


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
    
    def is_conda(self, strict=True):
        """Check whether this dependency can be managed by conda
        
        Args:
            strict (bool): whether only conda can manage this dep

        Returns:
            (bool)
        """
        if strict:
            return self.package_manager == 'conda'
        else:
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
        else:
            return self.package_manager is None or self.package_manager == 'pip'
    
    def fmt_conda_requirement(self):
        """Format dependency for conda requirements.yml files
        
        Returns:
            (str)
        """
        if self.is_conda(strict=False):
            if self.version is None:
                version = ""
            else:
                version = self.version
                if version[:2] in ('==', '>=', '<=', "~="):
                    logger.warning("bad version specification for '{}' with conda, use '=' by default".format(self.name))
                    version = "=" + version[2:]
                elif version[0] != '=':
                    version = "=" + version
            full_name = "{}{}".format(self.name, version)  # TODO channel
        elif self.is_pip(strict=True):
            if self.version is None:
                version = ""
            else:
                version = self.version
                if version[:2] not in ('==', '>=', '<=', "~="):
                    version = "==" + version
            full_name = "{}{}".format(self.name, version)
        else:  # TODO git url
            full_name = "# walou {}".format(self.name)
        
        return full_name
    
    def fmt_pip_requirement(self, extended=False):
        """Format dependency for pip requirements.txt files
        
        Returns:
            (str)
        """
        if self.is_pip(strict=False):
            if self.version is None:
                version = ""
            else:
                version = self.version
                if version[:2] not in ('==', '>=', '<=', "~="):
                    version = "==" + version
            full_name = "{}{}".format(self.name, version)
            txt = full_name
            if extended:
                txt += "  # pip install {}".format(full_name)
        elif self.is_conda(strict=True):
            if self.version is None:
                version = ""
            else:
                version = self.version
                if version[:2] in ('==', '>=', '<=', "~="):
                    logger.warning("bad version specification for '{}' with conda, use '=' by default".format(self.name))
                    version = "=" + version[2:]
                elif version[0] != '=':
                    version = "=" + version
            full_name = "{}{}".format(self.name, version)
            txt = "#{}".format(full_name)
            if extended:
                if self.channel is None:
                    txt += "  # conda install {}".format(full_name)
                else:
                    txt += "  # conda install -c {} {}".format(self.channel, full_name)
        else:  # assume valid git url
            txt = "#{}".format(self.name)
            if extended:
                txt += "  # pip install git+{}".format(self.package_manager)
        
        return txt
