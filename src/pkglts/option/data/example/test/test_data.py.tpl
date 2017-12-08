from os.path import basename
from os.path import join as pj

from {{ base.pkg_full_name }}.data_access import get, get_data_dir, ls
from {{ base.pkg_full_name }}.list_data import list_data


def test_data_access():
    assert basename(get_data_dir()) == "{{ base.pkgname }}_data"
    assert get("ext_data.txt").startswith("lorem ipsum")


def test_local_data():
    loc_names = list(list_data())
    for name in ("data.txt", "data.ui", "data.png"):
        assert name in loc_names
        assert pj("sub", "sub_%s" % name) in loc_names


def test_ext_data():
    ext_names = [name for name, is_dir in ls(".") if not is_dir]
    sub_ext_names = [name for name, is_dir in ls("sub") if not is_dir]
    for name in ("data.txt", "data.ui", "data.png"):
        assert "ext_%s" % name in ext_names
        assert "sub_ext_%s" % name in sub_ext_names
