from pkglts.dependency import Dependency

parameters = [
    ("classifiers", [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English"
    ])
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    classifiers = env.globals['pypi'].classifiers

    if len(classifiers) == 0:
        invalids.append("classifiers")

    return invalids


def require(purpose, env):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        env (jinja2.Environment):  current working environment

    Returns:
        (list of Dependency)
    """
    del env

    if purpose == 'option':
        options = ['pysetup']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        return [Dependency('twine', 'pip')]

    return []
