import mock

from pkglts.config_management import Config


class MockResponse:
    def __init__(self, status_code=500, json=None):
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json


def test_contributors_with_failed_request():
    with mock.patch('requests.get', return_value=MockResponse(status_code=500)):
        cfg = Config(dict(github={'owner': "moi", 'project': "project"}))
        cfg.load_extra()
        assert "failed" in cfg._env.globals['github'].contributors[0]


def test_contributors_without_failed_request():
    login = ['log1', 'log2']
    html_url = ['html_url1', 'html_url2']
    json = [{'login': login[0], 'html_url': html_url[0]}, {'login': login[1], 'html_url': html_url[1]}]
    with mock.patch('requests.get', return_value=MockResponse(status_code=200, json=json)):
        cfg = Config(dict(github={'owner': "moi", 'project': "project"}))
        cfg.load_extra()
        contributors = cfg._env.globals['github'].contributors
        assert len(contributors) == len(login)
        for i in range(0, len(contributors)):
            assert login[i] in contributors[i] and html_url[i] in contributors[i]
