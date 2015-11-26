from os import makedirs
from os.path import dirname, exists
from subprocess import call
from tuto_tools import initialize, rg

initialize()

from pkglts.manage import add_option, get_pkg_config, write_pkg_config

pkg_cfg = get_pkg_config()
pkg_cfg = add_option('pysetup', pkg_cfg)
pkg_cfg = add_option('data', pkg_cfg)

pkg_cfg['base']['pkgname'] = 'toto'
pkg_cfg['base']['namespace'] = None
pkg_cfg['pysetup']['intended_versions'] = ["27", "34", "35"]

write_pkg_config(pkg_cfg)

rg()

# write some data
for name in ("toto.txt", "titi.txt", "sub/tata.txt"):
    pth = "src/toto_data/" + name
    if not exists(dirname(pth)):
        makedirs(dirname(pth))

    with open(pth, 'w') as f:
        f.write("lorem ipsum\n")

call("python setup.py install", shell=True)
call("python ../test_data.py", shell=True)
