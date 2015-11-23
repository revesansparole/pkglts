parameters = [
    ("classifiers", ["Intended Audience :: Developers"])
]


def check(pkg_cfg):
    """Check the validity of parameters in package configuration.

    args:
     - pkg_cfg (dict of str, dict of str, any)): package configuration

    return:
     - (list of str): list of faulty parameters
    """
    invalids = []
    cfg = pkg_cfg['pypi']
    classifiers = cfg['classifiers']

    if len(classifiers) == 0:
        invalids.append("classifiers")

    return invalids
