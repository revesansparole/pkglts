# {# pkglts, data
""" Set of function to work with resources that are located inside
this package data
"""
from pathlib import Path


pkg_root_dir = Path(__file__).parent.parent
pkg_data_dir = pkg_root_dir / "{{ base.pkgname }}_data"
if not pkg_data_dir.exists():
    # we are certainly using a namespace
    pkg_root_dir = pkg_root_dir.parent
    pkg_data_dir = pkg_root_dir / "{{ base.pkgname }}_data"
    if not pkg_data_dir.exists():
        raise UserWarning(f"No data dir at this location: '{pkg_data_dir}'")


def get_data_dir():
    return pkg_data_dir


def get(file_name, mode='r'):
    """ Retrieve the content of a given filename
    located in the data part of this package.

    args:
     - file_name (str): name of the file to read
     - mode (str): mode to use to read the file either 'r' or 'rb'

    return:
       (str): content of the file red in 'r' mode
    """
    with open(pkg_data_dir / file_name, mode) as fhr:
        cnt = fhr.read()

    return cnt


def ls(dir_name):
    """ List all files and directories in dir_name
    located in the data part of this package.

    args:
     - dir_name (str): name of the directory to walk

    return:
       (list of [str, bool]): list the content of dir_name
                       without any specific order, items are
                       (entity_name, is_directory)
    """
    pth = pkg_data_dir / dir_name
    return [(n, n.is_dir()) for n in pth.iterdir()]

# #}
