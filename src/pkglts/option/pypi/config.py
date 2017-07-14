from pkglts.dependency import Dependency

parameters = [
    ("classifiers", [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English"
    ])
]


def check(cfg):
    """Check the validity of parameters in working environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    classifiers = cfg['pypi']['classifiers']

    if len(classifiers) == 0:
        invalids.append("classifiers")

    return invalids


def require(purpose, cfg):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        cfg (Config):  current package configuration

    Returns:
        (list of Dependency)
    """
    del cfg

    if purpose == 'option':
        options = ['pysetup']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        return [Dependency('twine', 'pip')]

    return []
