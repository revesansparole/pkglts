from os import remove
from os.path import exists
import pytest

from pkglts.file_management import write_file


@pytest.fixture()
def tmp_pth():
    pth = 'toto.txt'

    yield pth

    if exists(pth):
        remove(pth)


def test_write_file(tmp_pth):
    write_file(tmp_pth, "lorem ipsum")
    assert exists(tmp_pth)
