from tuto_tools import initialize, rg

initialize()

from pkglts.manage import add_option, get_pkg_config, write_pkg_config

pkg_cfg = get_pkg_config()
pkg_cfg = add_option('license', pkg_cfg)

cfg = pkg_cfg['base']
cfg['pkgname'] = 'toto'

write_pkg_config(pkg_cfg)

rg()
