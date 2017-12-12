import logging

logger = logging.getLogger(__name__)


class Dependency(object):
    """Simple container to keep track of all the required
    info to install a dependency.
    """
    
    def __init__(self, name, version="", pkg_mng=None, channel=None):
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
    
    def fmt_pip_requirement(self):
        """Format dependency for requirements files
        
        Returns:
            (str)
        """
        if self.is_pip(strict=False):
            version = self.version
            if version[:2] not in ('==', '>=', '<=', "~="):
                version = "==" + version
            full_name = "{}{}".format(self.name, version)
            txt = "{}  # pip install {}".format(full_name, full_name)
        elif self.is_conda(strict=True):
            version = self.version
            if version[:2] in ('==', '>=', '<=', "~="):
                logger.warning("bad version specification for '{}' with conda, use '=' by default".format(self.name))
                version = "=" + version[2:]
            elif version[0] != '=':
                version = "=" + version
            full_name = "{}{}".format(self.name, version)
            if self.channel is None:
                txt = "#{}  # conda install {}".format(full_name, full_name)
            else:
                txt = "#{}  # conda install -c {} {}".format(full_name, self.channel, full_name)
        else:  # assume valid git url
            txt = "#{}  # pip install git+{}".format(self.name, self.package_manager)
        
        return txt
