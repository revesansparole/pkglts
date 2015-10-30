from os.path import abspath, basename

from pkglts.option_tools import ask_arg


def is_valid_identifier(name):
    """ Check that name is a valid python identifier
    sort of back port of "".isidentifier()
    """
    try:
        compile("%s=1" % name, "test", 'single')
        return True
    except SyntaxError:
        return False


def main(pkg_cfg, extra):
    parent_dir = basename(abspath("."))
    pkg_fullname = ask_arg("base.pkg_fullname", pkg_cfg, parent_dir, extra)

    if "." in pkg_fullname:
        try:
            namespace, pkgname = pkg_fullname.split(".")
        except ValueError:
            raise UserWarning("package name not valid: %s" % pkg_fullname)

        if not is_valid_identifier(namespace) \
                or not is_valid_identifier(pkgname):
            raise UserWarning("package name not valid: %s" % pkg_fullname)
    else:
        namespace = None
        pkgname = pkg_fullname
        if not is_valid_identifier(pkg_fullname):
            raise UserWarning("package name not valid: %s" % pkg_fullname)

    owner = ask_arg("base.owner", pkg_cfg, "moi", extra)

    return dict(pkg_fullname=pkg_fullname,
                pkgname=pkgname,
                namespace=namespace,
                owner=owner)


def after(pkg_cfg):
    print("base: after main config")
