"""
Generate some files automatically
"""
from pathlib import Path

from pkglts.tree_ascii_fmt import fmt_tree

option_root_fld = Path("src/pkglts/option")
doc_fld = Path("doc/option")

for option_fld in sorted(option_root_fld.glob("*/")):
    option = option_fld.name
    if option_fld.is_dir() and not option.startswith("_"):
        print(option, option_fld)
        resource_fld = option_fld / 'resource'
        if not resource_fld.exists():
            print("this option does not create files")
        else:
            option_doc_fld = doc_fld / option
            if not option_doc_fld.exists():
                print(f"no doc found for {option}")
            else:
                txt = "<pre>\n" + fmt_tree(resource_fld) + "</pre>\n"
                print(txt)

                (option_doc_fld / "modifications.html").write_text(txt)
