from pkglts.versioning import get_github_version, get_local_version


print(__file__)


# TODO: bad tests requires internet connection
def test_get_github_version_returns_some_version_scheme():
    v = get_github_version()
    assert v >= '0.1.0'


def test_get_local_version_returns_some_version_scheme():
    v = get_local_version()
    assert v >= '0.1.0'
