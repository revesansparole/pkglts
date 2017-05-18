"""Generate a list of all available license templates
"""

from glob import glob
from os.path import basename, splitext


tpl_pth = "../../../src/pkglts/option/license/templates/*.txt"

with open("license_list.rst", 'w') as f:
    for pth in sorted(glob(tpl_pth)):
        name = splitext(basename(pth))[0]
        if not name.endswith("-header"):
            lines = [line.strip() for line in open(pth, 'rb').readlines() if len(line.strip()) > 0]
            txt = "\n".join("   " + line.decode("utf-8") for line in lines[:4])

            f.write("%s\n" % name)
            f.write("-" * len(name))
            f.write("\n\n")
            f.write("header::\n\n")
            f.write(txt)
            f.write("\n\n")
