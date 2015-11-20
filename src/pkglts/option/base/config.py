from os.path import abspath, basename


parameters = [
    ("pkgname", basename(abspath("."))),
    ("namespace", None),
    ("owner", "moi")
]


def is_valid_identifier(name):
    """ Check that name is a valid python identifier
    sort of back port of "".isidentifier()
    """
    try:
        compile("%s=1" % name, "test", 'single')
        return True
    except SyntaxError:
        return False


def check(pkg_cfg):
    """Check the validity of parameters in package configuration.

    args:
     - pkg_cfg (dict of str, dict of str, any)): package configuration

    return:
     - (list of str): list of faulty parameters
    """
    invalids = []
    pkgname = pkg_cfg['base']['pkgname']
    namespace = pkg_cfg['base']['namespace']

    if "." in pkgname:
        invalids.append('pkgname')
    elif not is_valid_identifier(pkgname):
        invalids.append('pkgname')

    if namespace is not None:
        if "." in namespace:
            invalids.append('namespace')
        elif not is_valid_identifier(namespace):
            invalids.append('namespace')

    return invalids


def after(pkg_cfg):
    del pkg_cfg  # unused
    print("base: after main config")
