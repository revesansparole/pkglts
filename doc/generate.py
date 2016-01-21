"""
Generate some files automatically
"""
from os import listdir
from os.path import isdir
from os.path import join as pj

from pkglts.tree_ascii_fmt import fmt_tree


base_pth = "src/pkglts_data/base"
doc_pth = "doc/option"

for option in listdir(base_pth):
    option_base_pth = pj(base_pth, option)
    if isdir(option_base_pth):
        print option
        option_doc_pth = pj(doc_pth, option)
        if not isdir(option_doc_pth):
            raise UserWarning("no doc found for %s" % option)

        txt = "<pre>\n" + fmt_tree(option_base_pth) + "</pre>\n"

        with open(pj(option_doc_pth, "modifications.html"), 'w') as f:
            f.write(txt)


