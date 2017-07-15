"""
Generate some files automatically
"""
from glob import glob
from os.path import basename, dirname, isdir, join as pj

from pkglts.tree_ascii_fmt import fmt_tree

base_pth = "src/pkglts_data/base"
doc_pth = "doc/option"

for option_base_pth in sorted(glob("{}/*/".format(base_pth))):
    option = basename(dirname(option_base_pth))
    if not option.startswith("_"):
        print(option)
        option_doc_pth = pj(doc_pth, option)
        if not isdir(option_doc_pth):
            print("no doc found for %s" % option)
        else:
            txt = "<pre>\n" + fmt_tree(option_base_pth) + "</pre>\n"

            with open(pj(option_doc_pth, "modifications.html"), 'w') as f:
                f.write(txt)
