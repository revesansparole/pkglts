from os.path import dirname

from pkglts.local import src_dir
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionSrc(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            namespace_method="pkg_util",
        )
        cfg['src'] = sec

    def check(self, cfg):
        invalids = []

        if cfg['src']['namespace_method'] not in ("pkg_util", "setuptools", "P3.3>"):
            invalids.append("src.namespace_method")

        return invalids

    def require_option(self):
        return ['base']

    def environment_extensions(self, cfg):
        return {
            "src_pth": src_dir(cfg)
        }
