from pathlib import Path

from pkglts.option_object import Option
from pkglts.version import __version__


class OptionGitlab(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        sec = dict(
            owner="{{ base.authors[0][0] }}",
            project="{{ base.pkgname }}",
            server="framagit.org",
            url="https://{{ gitlab.server }}/{{ gitlab.owner }}/{{ gitlab.project }}"
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        project = cfg[self._name]['project']

        if not project:
            invalids.append('gitlab.project')

        return invalids

    def require_option(self):
        return ['git']
