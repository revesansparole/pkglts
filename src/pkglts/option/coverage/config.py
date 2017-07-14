from pkglts.dependency import Dependency


def require(purpose, cfg):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        cfg (Config):  current package configuration

    Returns:
        (list of Dependency)
    """
    if purpose == 'option':
        options = ['test']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        deps = [Dependency('coverage')]
        test_suite = cfg['test']['suite_name']
        if test_suite == 'pytest':
            deps.append(Dependency('pytest-cov'))

        return deps

    return []
