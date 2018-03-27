"""
Generate some files automatically
"""
from glob import glob
from os.path import basename, dirname, isdir, join as pj

from pkglts.tree_ascii_fmt import fmt_tree

option_root_fld = "src/pkglts/option"
doc_fld = "doc/option"

for option_fld in sorted(glob("{}/*/".format(option_root_fld))):
    option = basename(dirname(option_fld))
    if not option.startswith("_"):
        print(option, option_fld)
        resource_fld = pj(option_fld, 'resource')
        if not isdir(resource_fld):
            print("this option does not create files")
        else:
            option_doc_fld = pj(doc_fld, option)
            if not isdir(option_doc_fld):
                print("no doc found for %s" % option)
            else:
                txt = "<pre>\n" + fmt_tree(resource_fld) + "</pre>\n"
                print(txt)

                with open(pj(option_doc_fld, "modifications.html"), 'w') as f:
                    f.write(txt)
