from nose.tools import assert_raises

from pkglts.file_management import get_revision

print(__file__)


def test_revision_return_none_if_no_rev():
    txt = """
print 'toto'
print 'rev'
"""
    assert get_revision(txt) is None


def test_revision_find_rev_tag1():
    txt = """# rev = 1
print 'titi'
assert False
"""
    assert get_revision(txt) == 1


def test_revision_find_rev_tag2():
    txt = """print 'tata'
# rev = 1
print 'titi'
assert False
"""
    assert get_revision(txt) == 1


def test_revision_find_rev_tag3():
    txt = """
print 'tata'
# rev = 1
print 'titi'
assert False
"""
    assert get_revision(txt) == 1


def test_revision_requires_integer1():
    txt = """# rev = 'a'
print 'titi'
"""
    assert_raises(ValueError, lambda: get_revision(txt))


def test_revision_requires_integer2():
    txt = """# rev = 1.2
print 'titi'
"""
    assert_raises(ValueError, lambda: get_revision(txt))
