from nose.tools import with_setup
from os import remove
from os.path import exists

from pkglts.file_management import write_file, user_modified

print(__file__)

ex_file = 'toto.txt'


def teardown():
    if exists(ex_file):
        remove(ex_file)


@with_setup(teardown=teardown)
def test_write_file_register_hash():  # TODO less specific implementation
    txt = """
print 'toto'
print 'rev'
"""
    hm = {}
    write_file(ex_file, txt, hm)
    assert ex_file in hm


@with_setup(teardown=teardown)
def test_non_registered_file_appears_as_user_modified():
    with open(ex_file, 'w') as f:
        f.write("lorem ipsum\n")

    assert user_modified(ex_file, {})


@with_setup(teardown=teardown)
def test_newly_created_file_not_user_modified():
    content = "lorem ipsum\n" * 10
    hm = {}

    write_file(ex_file, content, hm)

    assert not user_modified(ex_file, hm)


@with_setup(teardown=teardown)
def test_tempering_detected():
    txt = """
print 'toto'
print 'rev'
"""
    hm = {}
    write_file(ex_file, txt, hm)
    assert not user_modified(ex_file, hm)
    txt = txt[:3] + '#' + txt[4:]
    with open(ex_file, 'w') as f:
        f.write(txt)

    assert user_modified(ex_file, hm)
