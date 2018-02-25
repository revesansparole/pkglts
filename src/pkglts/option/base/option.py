from os.path import abspath, basename, dirname

from pkglts.local import pkg_full_name, src_dir
from pkglts.option_object import Option


def is_valid_identifier(name):
    """ Check that name is a valid python identifier
    sort of back port of "".isidentifier()
    """
    try:
        compile("%s=1" % name, "test", 'single')
        return True
    except SyntaxError:
        return False


class OptionBase(Option):
    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            pkgname=basename(abspath(".")),
            namespace=None,
            namespace_method="pkg_util",
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

        if cfg['base']['namespace_method'] not in ("pkg_util", "setuptools", "P3.3>"):
            invalids.append("base.namespace_method")

        return invalids

    def environment_extensions(self, cfg):
        return {"pkg_full_name": pkg_full_name(cfg),
                "src_pth": src_dir(cfg)}
