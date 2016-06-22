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
