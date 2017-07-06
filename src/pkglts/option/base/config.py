from os.path import abspath, basename

from pkglts.dependency import Dependency

parameters = [
    ("pkgname", basename(abspath("."))),
    ("namespace", None),
    ("namespace_method", "pkg_util"),
    ("url", None),
    ("authors", [("moi", "moi@email.com")])
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


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    pkgname = env.globals['base'].pkgname
    namespace = env.globals['base'].namespace

    if "." in pkgname:
        invalids.append('pkgname')
    elif not is_valid_identifier(pkgname):
        invalids.append('pkgname')

    if namespace is not None:
        if "." in namespace:
            invalids.append('namespace')
        elif not is_valid_identifier(namespace):
            invalids.append('namespace')

    if env.globals['base'].namespace_method not in ("pkg_util", "setuptools", "P3.3>"):
        invalids.append("namespace_method")

    return invalids


def after(pkg_cfg):
    del pkg_cfg  # unused
    print("base: after main config")


def require(purpose, env):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        env (jinja2.Environment):  current working environment

    Returns:
        (list of Dependency)
    """
    del env, purpose

    return []
