from os.path import join as pj

from {{base.pkg_full_name, }}.data_access import ls
from {{base.pkg_full_name, }}.list_data import list_data


def test_local_data():
    loc_names = list(list_data())
    for name in ("data.txt", "data.ui", "data.png"):
        assert name in loc_names
        assert pj("sub", "sub_%s" % name) in loc_names


def test_ext_data():
    ext_names = ls(".")
    print "ext", ext_names