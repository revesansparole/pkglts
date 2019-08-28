from os.path import dirname
from pkglts.option_object import Option
from pkglts.version import __version__

from . import bump_version


class OptionVersion(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            major=0,
            minor=0,
            post=1,
        )
        cfg['version'] = sec

    def check(self, cfg):
        invalids = []
        major = cfg['version']['major']
        minor = cfg['version']['minor']
        post = cfg['version']['post']

        if not isinstance(major, int):
            invalids.append("version.major")
        if not isinstance(minor, int):
            invalids.append("version.minor")
        if not isinstance(post, int):
            invalids.append("version.post")

        return invalids

    def require_option(self):
        return ['src']

    def tools(self, cfg):
        del cfg
        yield bump_version.parser_bump
