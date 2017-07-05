class Dependency(object):
    """Simple container to keep track of all the required
    info to install a dependency.
    """
    def __init__(self, name, pkg_mng=None, channel=None):
        self.name = name  # name of dependency
        self.package_manager = pkg_mng  # either conda, pip or git url
        self.channel = channel  # place to find the dependency depends on package_manager
