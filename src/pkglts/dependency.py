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
    
    def is_conda(self):
        return self.package_manager is None or self.package_manager == 'conda'
    
    def is_pip(self):
        return self.package_manager == 'pip'
    
    def fmt_requirement(self):
        """Format dependency for requirements files
        
        Returns:
            (str)
        """
        if self.package_manager is None:
            pkg_mng = "conda"
        else:
            pkg_mng = self.package_manager
        
        if pkg_mng == "conda":
            if self.channel is None:
                install_cmd = "conda install {}".format(self.name)
            else:
                install_cmd = "conda install -c {} {}".format(self.channel, self.name)
        elif pkg_mng == "pip":
            install_cmd = "pip install {}".format(self.name)
        else:  # assume valid git url
            install_cmd = "pip install git+{}".format(pkg_mng)
        
        return "{} # {}".format(self.name, install_cmd)
