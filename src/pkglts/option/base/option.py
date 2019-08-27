from os.path import abspath, basename, dirname

from pkglts.local import pkg_full_name
from pkglts.option_object import Option
from pkglts.small_tools import is_valid_identifier
from pkglts.version import __version__


class OptionBase(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            pkgname=basename(abspath(".")),
            namespace=None,
            url=None,
            authors=[("moi", "moi@email.com")]
        )
        cfg['base'] = sec

    def check(self, cfg):
        invalids = []
        pkgname = cfg['base']['pkgname']
        namespace = cfg['base']['namespace']

        if "." in pkgname:
            invalids.append('base.pkgname')
        elif not is_valid_identifier(pkgname):
            invalids.append('base.pkgname')

        if namespace is not None:
            if "." in namespace:
                invalids.append('base.namespace')
            elif not is_valid_identifier(namespace):
                invalids.append('base.namespace')

        return invalids

    def environment_extensions(self, cfg):
        return {"pkg_full_name": pkg_full_name(cfg)}
