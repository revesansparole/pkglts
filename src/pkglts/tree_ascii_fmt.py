from os import listdir
from os.path import abspath, basename, isdir
from os.path import join as pj

from pkglts.local import load_all_handlers
from pkglts.templating import replace


def nn(pth):
    pkg_cfg = dict(base={"namespace": None,
                         "owner": "owner",
                         "pkgname": "pkgname",
                         "url": None})
    handlers = load_all_handlers(pkg_cfg)
    tgt_name = replace(pth, handlers, pkg_cfg)
    if tgt_name.endswith(".tpl"):
        tgt_name = tgt_name[:-4]

    return tgt_name


def tree(dir, padding, txt):
    txt += padding[:-1] + '+-' + nn(basename(abspath(dir))) + '/\n'
    padding += ' '
    files = [(isdir(pj(dir, file)), file) for file in listdir(dir)]
    files.sort()

    count = 0
    for is_dir, file in files:
        count += 1
        txt += padding + '|\n'
        path = pj(dir, file)
        if is_dir:
            if count == len(files):
                txt = tree(path, padding + ' ', txt)
            else:
                txt = tree(path, padding + '|', txt)
        else:
            txt += padding + '+-' + nn(file) + '\n'

    return txt


def fmt_tree(dir):
    return tree(dir, ' ', "")

# txt = tree("../src/pkglts_data/base", ' ', "")
# print txt
