from nose.tools import with_setup
from os import remove
from os.path import exists
from string import Template

from pkglts.file_management import get_hash, write_file

print(__file__)

ex_file = 'toto.txt'


def teardown():
    if exists(ex_file):
        remove(ex_file)


# @with_setup(teardown=teardown)
# def test_get_hash_change_with_content():
#     with open(ex_file, 'w') as f:
#         f.write("toto")
#
#     h1 = get_hash(ex_file)
#
#     with open(ex_file, 'w') as f:
#         f.write("toto addendum")
#
#     h2 = get_hash(ex_file)
#
#     assert h1 != h2


def test_get_hash_use_only_non_user_divs_for_hash():
    txt = Template("""
before = 1
$in1
# {{rm, $in2}}
middle = 1
# {{pkglts rm, $in3}}
after = 1
# {{pkglts upper,
$in4
# }}
""")
    with open(ex_file, 'w') as f:
        f.write(txt.substitute(in1="1", in2="2", in3="3", in4="4"))

    href = get_hash(ex_file)

    with open(ex_file, 'w') as f:
        f.write(txt.substitute(in1="M", in2="2", in3="3", in4="4"))

    assert get_hash(ex_file) == href

    with open(ex_file, 'w') as f:
        f.write(txt.substitute(in1="1", in2="M", in3="3", in4="4"))

    assert get_hash(ex_file) == href

    with open(ex_file, 'w') as f:
        f.write(txt.substitute(in1="1", in2="2", in3="M", in4="4"))

    assert get_hash(ex_file) != href
    assert get_hash(ex_file)[1] == href[1]

    with open(ex_file, 'w') as f:
        f.write(txt.substitute(in1="1", in2="2", in3="3", in4="M"))

    assert get_hash(ex_file) != href
    assert get_hash(ex_file)[0] == href[0]


# @with_setup(teardown=teardown)
# def test_write_file_register_hash():  # TODO less specific implementation
#     txt = """
# print 'toto'
# print 'rev'
# """
#     hm = {}
#     write_file(ex_file, txt, hm)
#     assert ex_file in hm
#
#
# @with_setup(teardown=teardown)
# def test_non_registered_file_appears_as_user_modified():
#     with open(ex_file, 'w') as f:
#         f.write("lorem ipsum\n")
#
#     assert user_modified(ex_file, {})
#
#
# @with_setup(teardown=teardown)
# def test_newly_created_file_not_user_modified():
#     content = "lorem ipsum\n" * 10
#     hm = {}
#
#     write_file(ex_file, content, hm)
#
#     assert not user_modified(ex_file, hm)
#
#
# @with_setup(teardown=teardown)
# def test_tempering_detected():
#     txt = """
# print 'toto'
# print 'rev'
# """
#     hm = {}
#     write_file(ex_file, txt, hm)
#     assert not user_modified(ex_file, hm)
#     txt = txt[:3] + '#' + txt[4:]
#     with open(ex_file, 'w') as f:
#         f.write(txt)
#
#     assert user_modified(ex_file, hm)
