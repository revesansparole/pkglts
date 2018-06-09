from os import remove
from os.path import exists
import pytest

from pkglts.hash_management import compute_hash, modified_file_hash, pth_as_key


@pytest.fixture()
def tmp_pth():
    pth = 'toto.txt'

    yield pth

    if exists(pth):
        remove(pth)


def test_pth_as_key_produce_unique_path():
    pth1 = pth_as_key("./toto/titi/")
    pth2 = pth_as_key("toto/titi")
    pth3 = pth_as_key("./toto/../toto/titi")

    assert pth1 == pth2
    assert pth1 == pth3


def test_compute_hash():
    assert compute_hash("toto") == compute_hash("toto")
    assert compute_hash("toto") != compute_hash("titi")


def test_modified_file_raise_error_if_file_not_in_hashmap(tmp_pth):
    with open(tmp_pth, 'w') as f:
        f.write("lorem ipsum\n" * 10)

    with pytest.raises(IOError):
        modified_file_hash(tmp_pth, {})


def test_modified_file_detect_modifications_only_in_preserved_sections(tmp_pth):
    with open(tmp_pth, 'w') as f:
        f.write("lorem ipsum\n" * 10)

    assert not modified_file_hash(tmp_pth, {tmp_pth: []})


def test_modified_file_if_not_same_preserved_sections(tmp_pth):
    txt = "lorem ipsum\n" * 10

    with open(tmp_pth, 'w') as f:
        f.write("{# pkglts, toto\n")
        f.write(txt)
        f.write("#}\n")

    assert modified_file_hash(tmp_pth, {tmp_pth: dict(titi="azerty")})


def test_modified_file_detect_modifications_in_preserved_sections(tmp_pth):
    txt = "lorem ipsum\n" * 10
    hv = compute_hash(txt)

    with open(tmp_pth, 'w') as f:
        f.write("{# pkglts, toto\n")
        f.write(txt)
        f.write("#}\n")

    assert not modified_file_hash(tmp_pth, {tmp_pth: dict(toto=hv)})

    with open(tmp_pth, 'w') as f:
        f.write("{# pkglts, toto\n")
        f.write(txt * 2)
        f.write("#}\n")

    assert modified_file_hash(tmp_pth, {tmp_pth: dict(toto=hv)})
