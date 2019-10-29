"""Generate a list of all available license templates
"""
from pathlib import Path

import pkglts

tpl_pth = Path(pkglts.__file__).parent / "option/license/templates"

with open("license_list.rst", 'w') as f:
    for pth in tpl_pth.glob("*.txt"):
        name = pth.name.split(".")[0]
        if not name.endswith("-header"):
            lines = [line.strip() for line in open(pth, 'rb').readlines() if len(line.strip()) > 0]
            txt = "\n".join("   " + line.decode("utf-8") for line in lines[:4])

            f.write(f"{name}\n")
            f.write("-" * len(name))
            f.write("\n\n")
            f.write("header::\n\n")
            f.write(txt)
            f.write("\n\n")
