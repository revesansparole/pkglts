import logging
from pathlib import Path

from pkglts.local import pkg_full_name
from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionBase(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        LOGGER.info("update parameters %s", self._name)
        sec = dict(
            pkgname=Path.cwd().name,
            namespace=None,
            url=None,
            authors=[("moi", "moi@email.com")]
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        pkgname = cfg[self._name]['pkgname']
        namespace = cfg[self._name]['namespace']

        if "." in pkgname:
            invalids.append('base.pkgname')
        elif not pkgname.isidentifier():
            invalids.append('base.pkgname')

        if namespace is not None:
            if "." in namespace:
                invalids.append('base.namespace')
            elif not namespace.isidentifier():
                invalids.append('base.namespace')

        return invalids

    def environment_extensions(self, cfg):
        return {"pkg_full_name": pkg_full_name(cfg)}
