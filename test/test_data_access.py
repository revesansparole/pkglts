from os.path import basename

from pkglts.data_access import get, get_data_dir, ls


def test_data_access_data_dir():
    assert basename(get_data_dir()) == "pkglts_data"


def test_data_access_ls():
    assert (set(ls('test/test1')) == {('subtest', True), ('titi.txt', False)})


def test_data_access_get():
    assert get('test/toto.txt').rstrip() == "lorem ipsum"
