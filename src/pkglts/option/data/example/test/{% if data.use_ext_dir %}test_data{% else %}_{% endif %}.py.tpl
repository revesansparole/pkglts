from {{ base.pkg_full_name }}.data_access import get, get_data_dir, ls


def test_data_access():
    assert get_data_dir().name == "{{ base.pkgname }}_data"
    assert get("ext_data.txt").startswith("lorem ipsum")


def test_ext_data():
    ext_names = [pth.name for pth, is_dir in ls(".") if not is_dir]
    sub_ext_names = [pth.name for pth, is_dir in ls("sub") if not is_dir]
    for name in ("data.txt", "data.ui", "data.png"):
        assert f"ext_{name}" in ext_names
        assert f"sub_ext_{name}" in sub_ext_names
