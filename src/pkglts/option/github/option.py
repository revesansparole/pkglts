from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option


class OptionGithub(Option):
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

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['git']
            return [Dependency(name) for name in options]

        return []
