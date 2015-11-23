from pkglts.rmtfile import get, ls


def test_rmtfile_ls():
    assert (set(ls('pkglts_data/test/test1')) ==
            {('subtest', True), ('titi.txt', False)})


def test_rmtfile_get():
    assert get('pkglts_data/test/toto.txt').rstrip() == "lorem ipsum"
