from os.path import dirname

from pkglts.option_object import Option
from pkglts.version import __version__


class OptionGithub(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            owner="{{ base.authors[0][0] }}",
            project="{{ base.pkgname }}",
            url="https://github.com/{{ github.owner }}/{{ github.project }}"
        )
        cfg['github'] = sec

    def check(self, cfg):
        invalids = []
        project = cfg['github']['project']

        if not project:
            invalids.append('github.project')

        return invalids

    def require_option(self):
        return ['git']
