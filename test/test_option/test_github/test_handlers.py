import mock

from pkglts.config_management import Config


def test_contributors_with_failed_request():
    with mock.patch('subprocess.check_output', side_effect=KeyError):
        cfg = Config(dict(github={'owner': "moi", 'project': "project"}))
        cfg.load_extra()
        assert "failed" in cfg._env.globals['github'].contributors[0]


def test_contributors_without_failed_request():
    commits = b'commit Author: a <toto@titi>\n, commit: Author: b <tata@titi>\n, commit: Author: b <tata@titi>\n'
    with mock.patch('subprocess.check_output', return_value=commits):
        cfg = Config(dict(github={'owner': "moi", 'project': "project"}))
        cfg.load_extra()
        contributors = cfg._env.globals['github'].contributors
        assert len(contributors) == 2
