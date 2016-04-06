"""Generate a list of all available license templates
"""

from glob import glob
from os.path import basename, splitext


tpl_pth = "../../../src/pkglts/option/license/templates/*.txt"

with open("license_list.rst", 'w') as f:
    for pth in sorted(glob(tpl_pth)):
        name = splitext(basename(pth))[0]
        if not name.endswith("-header"):
            f.write("  * %s\n" % name)
