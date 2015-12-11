from os.path import exists

from .handlers import get_tpl_path


parameters = [
    ("name", "cecill-c"),
    ("year", 2015),
    ("organization", "organization"),
    ("project", "{{key, base.pkgname}}")
]


def check(pkg_cfg):
    """Check the validity of parameters in package configuration.

    args:
     - pkg_cfg (dict of str, dict of str, any)): package configuration

    return:
     - (list of str): list of faulty parameters
    """
    invalids = []
    name = pkg_cfg['license']['name']
    # year = pkg_cfg['license']['year']
    # organization = pkg_cfg['license']['organization']
    # project = pkg_cfg['license']['project']

    if len(name) == 0:
        invalids.append('name')
    elif not exists(get_tpl_path(name)):
        invalids.append('name')

    return invalids
