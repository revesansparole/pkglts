# rev = 1
""" Contains functions to manage the structure of the package.

Use 'setup.py' for common tasks.
"""

import json
from os import listdir, remove, walk
from os.path import exists, isdir, splitext
from os.path import join as pj
from shutil import rmtree

from .local import load_all_handlers, installed_options
from .manage_tools import (create_package_hash_keys,
                           clone_base_option, clone_example, regenerate_pkg,
                           update_opt)
from .option_tools import get_user_permission
from .templating import get_comment_marker, replace
from .versioning import get_github_version, get_local_version


pkg_cfg_file = "pkg_cfg.json"
pkg_hash_file = "pkg_hash.json"


def init_pkg(rep="."):
    """ Initialise a package in given directory
    """
    if not exists(pkg_cfg_file):
        write_pkg_config({}, rep)
    if not exists(pkg_hash_file):
        write_pkg_hash({}, rep)


def get_pkg_config(rep="."):
    """ Read pkg_cfg file associated to this package

    args:
     - rep (str): directory to search for info

    return:
     - (dict of (str, dict)): option_name: options
    """
    with open(pj(rep, pkg_cfg_file), 'r') as f:
        info = json.load(f)

    return info


def write_pkg_config(pkg_cfg, rep="."):
    """ Store config associated to this package on disk

    args:
     - pkg_cfg (dict of (str, dict)): option_name, options
     - rep (str): directory to search for info
    """
    cfg = dict(pkg_cfg)
    for key in tuple(cfg.keys()):
        if key.startswith("_"):
            del cfg[key]

    with open(pj(rep, pkg_cfg_file), 'w') as f:
        json.dump(cfg, f, sort_keys=True, indent=4)


def get_pkg_hash(rep="."):
    """ Read pkg_hash file associated to this package

    args:
     - rep (str): directory to search for info

    return:
     - (dict of (str, hash)): file path: hash key
    """
    with open(pj(rep, pkg_hash_file), 'r') as f:
        hm = json.load(f)

    return dict((pth, tuple(key)) for pth, key in hm.items())


def write_pkg_hash(pkg_hash, rep="."):
    """ Store hash associated to this package on disk

    args:
     - pkg_hash (dict of (str, hash)): file path: hash key
     - rep (str): directory to search for info
    """
    cfg = dict(pkg_hash)

    # remove unwanted keys
    # for key in tuple(cfg.keys()):
    #     if key.startswith("_"):
    #         del cfg[key]

    with open(pj(rep, pkg_hash_file), 'w') as f:
        json.dump(cfg, f, sort_keys=True, indent=4)


def clean(rep="."):
    """ Thorough cleaning of all arborescence rooting at rep.

    # TODO: exception list instead of hardcoded one

    args:
     - rep (str): default ".", top directory to clean
    """
    for name in ("build", "dist"):
        pth = pj(rep, name)
        if exists(pth):
            rmtree(pth)

    for root, dnames, fnames in walk(rep):
        # do not walk directories starting with "."
        for name in tuple(dnames):
            if "clean.no" in listdir(pj(root, name)):
                dnames.remove(name)
            elif name.startswith("."):
                dnames.remove(name)
            elif name == "__pycache__":
                rmtree(pj(root, name))
                dnames.remove(name)

        for name in fnames:
            if not name.startswith("."):
                if splitext(name)[1] in [".pyc", ".pyo"]:
                    remove(pj(root, name))


def update_pkg(pkg_cfg):
    """ Check if a new version of ltspkg exists
    """
    gth_ver = get_github_version()
    loc_ver = get_local_version()
    if gth_ver <= loc_ver:
        print("package is up to date, nothing to do")
    else:
        print("newer version of package available")
        if get_user_permission("install"):
            print("install")
            # TODO: perform installation
            # if get_user_permission('develop mode'):
            #     print("update your code before continuing")
            #     get_user_permission("continue")
            # else:
            #     pip_args = ['-vvv']
            #     proxy = os.environ['http_proxy']
            #     if proxy:
            #         pip_args.append('--proxy')
            #         pip_args.append(proxy)
            #     pip_args.append('install')
            #     pip_args.append('pkglts')
            #     pip.main(pip_args)
        else:
            return pkg_cfg

        # relaunch config for each installed option
        for opt_name in installed_options(pkg_cfg):
            pkg_cfg = update_option(opt_name, pkg_cfg)

        # regenerate will be called explicitly

    return pkg_cfg


def update_option(name, pkg_cfg):
    """ Update an already installed option

    args:
     - name (str): name of option to update
     - pkg_cfg (dict of (str, dict)): option_name, options
    """
    if name not in pkg_cfg:
        raise UserWarning("Option '%s' seems not to be installed" % name)

    extra = pkg_cfg[name]  # one way to re-force already set args

    return update_opt(name, pkg_cfg, extra)


def edit_option(name, pkg_cfg):
    """ Edit an already installed option

    args:
     - name (str): name of option to update
     - pkg_cfg (dict of (str, dict)): option_name, options
    """
    if name not in pkg_cfg:
        raise UserWarning("Option '%s' seems not to be installed" % name)

    return update_opt(name, pkg_cfg)


def add_option(name, pkg_cfg, extra=None):
    """ Add a new option to this package.
    See the list of available option online

    args:
     - name (str): name of option to add
     - pkg_cfg (dict of (str, dict)): package configuration parameters
     - extra (dict): extra arguments for option configuration
    """
    if name in pkg_cfg:
        raise UserWarning("option already included in this package")

    return update_opt(name, pkg_cfg, extra)


def install_example_files(option, pkg_cfg, target="."):
    if option is None:
        return None

    if option not in pkg_cfg:
        print("please install option before example files")
        return None

    # get handlers
    h = load_all_handlers(pkg_cfg)

    root = "pkglts_data/example/%s" % option
    # walk all files in example repo to copy them handling conflicts on the way
    clone_example(root, target, pkg_cfg, h)


# def regenerate_file(name, pkg_cfg, handlers):
#     """ Parse the content of a file for {{div}}
#     use handlers to modify the content and rewrite file
#
#     args:
#      - name (str): name of file to scan/modify
#      - pkg_cfg (dict of (str, dict)): package configuration parameters
#      - handlers (dict of (str, handler)): functions used to modify text
#     """
#     print "reg", name
#     with open(name, 'r') as f:
#         src_content = f.read()
#
#     new_src_content = replace(src_content, handlers, pkg_cfg,
#                               get_comment_marker(name))
#
#     # overwrite file without any warning
#     if "modif" in name:
#         new_name = name
#     else:
#         new_name = name[:-4] + "_modif" + name[-4:]
#     with open(new_name, 'w') as f:
#         f.write(new_src_content)
#

# def regenerate(pkg_cfg, target=".", overwrite=False):
#     """ Rebuild all automatically generated files
#
#     args:
#      - pkg_cfg (dict of (str, dict)): package configuration parameters
#      - target (str): target directory to write into
#      - overwrite (bool): default False, whether or not
#                          to overwrite user modified files
#     """
#     # parse options and load handlers
#     handlers = load_all_handlers(pkg_cfg)
#
#     root = "pkglts_data/base"
#     if not overwrite:
#         # walk all files in repo to check for possible tempering
#         # of files by user
#         tf = []
#         check_tempering(root, target, handlers, pkg_cfg, tf)
#         if len(tf) > 0:
#             msg = "These files have been modified by user:\n"
#             msg += "\n".join(tf)
#             raise UserWarning(msg)
#
#     # walk all files in repo and regenerate them
#     regenerate_dir(root, target, handlers, pkg_cfg, True)
#
#     # walk all files in package and replace div inside if needed
#     # TODO: use gitignore to ignore some directories/files
#     if "regenerate.no" not in listdir(target):
#         for fname in listdir(target):
#             if not isdir(pj(target, fname)):
#                 regenerate_file(pj(target, fname), pkg_cfg, handlers)
#
#     for dname in ("doc", "src", "test"):
#         if "regenerate.no" not in listdir(dname):
#             for pdir, dnames, fnames in walk(pj(target, dname)):
#                 for name in tuple(dnames):
#                     if "regenerate.no" in listdir(pj(pdir, name)):
#                         dnames.remove(name)
#
#                 for name in fnames:
#                     if splitext(name) not in (".pyc", ".pyo"):
#                         regenerate_file(pj(pdir, name), pkg_cfg, handlers)


def regenerate(pkg_cfg, target=".", overwrite=False):
    """ Rebuild all automatically generated files

    args:
     - pkg_cfg (dict of (str, dict)): package configuration parameters
     - target (str): target directory to write into
     - overwrite (bool): default False, whether or not
                         to overwrite user modified files
    """
    handlers = load_all_handlers(pkg_cfg)

    # check for potential conflicts
    hm_ref = get_pkg_hash(target)
    hm = create_package_hash_keys(pkg_cfg, target)
    conflicted = []
    for pth, ref_key in hm_ref.items():
        try:
            key = hm[pth]
            if key != ref_key:
                conflicted.append(pth)
        except KeyError:
            # file apparently not managed by pkglts
            pass

    overwrite_file = {}
    if len(conflicted) > 0:
        print("conflicted", conflicted)
        if overwrite:
            for name in conflicted:
                overwrite_file[name] = True
        else:
            for name in conflicted:
                print("A non editable section of %s has been modified" % name)
                overwrite_file[name] = get_user_permission("overwrite", False)

    # copy all missing files for options
    # regenerating pkglts divs on the way
    for option in installed_options(pkg_cfg):
        clone_base_option(option, pkg_cfg, handlers, target, overwrite_file)

    # regenerate files
    regenerate_pkg(pkg_cfg, handlers, target, overwrite_file)

    # re create hash
    hm = create_package_hash_keys(pkg_cfg, target)
    write_pkg_hash(hm, target)
