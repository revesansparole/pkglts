from nose.tools import with_setup
from os import remove
from os.path import exists

from pkglts.file_management import write_file


ex_file = 'toto.txt'


def teardown():
    if exists(ex_file):
        remove(ex_file)


@with_setup(teardown=teardown)
def test_write_file():
    write_file(ex_file, "lorem ipsum")
    assert exists(ex_file)

