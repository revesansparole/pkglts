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
    
    def fmt_pip_requirement(self):
        """Format dependency for requirements files
        
        Returns:
            (str)
        """
        if self.package_manager is None:
            pkg_mng = "conda"
        else:
            pkg_mng = self.package_manager
        
        if self.version is None:
            full_name = self.name
        else:
            version = self.version
            if pkg_mng == 'conda':
                if version[:2] in ('==', '>=', '<=', "~="):
                    logger.warning("bad version specification for '{}' with conda, use '=' by default".format(self.name))
                    version = "=" + self.version[2:]
            full_name = "{}{}".format(self.name, version)
        
        if pkg_mng == "conda":
            if self.channel is None:
                install_cmd = "conda install {}".format(full_name)
            else:
                install_cmd = "conda install -c {} {}".format(self.channel, full_name)
        elif pkg_mng == "pip":
            install_cmd = "pip install {}".format(full_name)
        else:  # assume valid git url
            install_cmd = "pip install git+{}".format(pkg_mng)
        
        return "{} # {}".format(full_name, install_cmd)
