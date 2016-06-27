from pkglts.hash_management import pth_as_key


def test_pth_as_key_produce_unique_path():
    pth1 = pth_as_key("./toto/titi/")
    pth2 = pth_as_key("toto/titi")
    pth3 = pth_as_key("./toto/../toto/titi")

    assert pth1 == pth2
    assert pth1 == pth3
