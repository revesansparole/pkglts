from pathlib import Path

from {{ base.pkg_full_name }}.list_data import list_data


def test_local_data():
    loc_names = list(list_data())
    for name in ("data.txt", "data.ui", "data.png"):
        assert Path(name) in loc_names
        assert Path(f"sub/sub_{name}") in loc_names
