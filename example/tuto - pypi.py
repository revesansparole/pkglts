from tuto_tools import initialize, rg

initialize()

from pkglts.manage import add_option, get_pkg_config, write_pkg_config

pkg_cfg = get_pkg_config()
pkg_cfg = add_option('pypi', pkg_cfg)

pkg_cfg['base']['pkgname'] = 'toto'
pkg_cfg['pysetup']['intended_versions'] = ["27", "34", "35"]

write_pkg_config(pkg_cfg)

rg()
