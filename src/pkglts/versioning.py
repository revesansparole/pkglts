from distutils.version import StrictVersion
try:
    from urllib.request import urlopen, URLError
except ImportError:
    from urllib2 import urlopen, URLError

github_url = ("https://raw.githubusercontent.com/revesansparole/"
              "pkglts/master/src/pkglts/version.py")


def get_github_version():
    """ Fetch the current version of this package on master branch
     on github.
    """
    try:
        response = urlopen(github_url)
        pycode = response.read()

        ast = compile(pycode, "<file>", 'exec')
        d = {}
        eval(ast, d)

        return StrictVersion(d['__version__'])
    except URLError:
        return None


def get_local_version():
    """ Fetch the current installed version of this package
    """
    import pkglts
    return StrictVersion(pkglts.__version__)


def upgrade_pkg_cfg_version(pkg_cfg, version):
    """Upgrade the version of pkg_cfg file from version to version +1

    Args:
        pkg_cfg (dict of str: any): package configuration
        version (int): current version of file

    Returns:
        (dict of str: any): a reference to an updated pkg_cfg
    """
    if version == 0:
        pkg_cfg['_pkglts']['version'] = 1
    elif version == 1:
        try:
            sphinx_cfg = pkg_cfg['sphinx']
            sphinx_cfg['autodoc-dvlpt'] = sphinx_cfg.get('autodoc-dvlpt', True)
        except KeyError:
            pass

        pkg_cfg['_pkglts']['version'] = 2

    return pkg_cfg
