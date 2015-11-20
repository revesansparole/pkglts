""" Specific helper function for manage script
"""

import imp
from importlib import import_module
from os import listdir, mkdir, walk
from os.path import basename, exists, isdir
import pip
from pip import get_installed_distributions
from pip import main as pip_install

from .file_management import get_hash, write_file
from .local import init_namespace_dir
from .option_tools import get_user_permission
from .rmtfile import get, ls
from .templating import (closing_marker, get_comment_marker, opening_marker,
                         replace, swap_divs)


tpl_src_name = "%skey, base.pkgname%s" % (opening_marker, closing_marker)


def ensure_installed_packages(requirements, msg):
    """ Ensure all packages in requirements are installed.

    If not, ask user permission to install them.

    args:
     - requirements (list of str): list of package names to pip install
                                   if needed
    """
    pip.util.pkg_resources = imp.reload(pip.util.pkg_resources)
    installed = set(p.project_name for p in get_installed_distributions())
    to_install = set(requirements) - installed
    if len(to_install) > 0:
        print(msg)
        print("missing packages: " + ", ".join(to_install))
        if get_user_permission("install"):
            pip_install(['install'] + list(to_install))
            return True
        else:
            return False
    return True


def update_opt(name, pkg_cfg, extra=None):
    """ Update an option of this package. If the option
    does not exists yet, add it first.
    See the list of available option online

    args:
     - name (str): name of option to add
     - pkg_cfg (dict of (str, dict)): package configuration parameters
     - extra (dict): extra arguments for option configuration
    """
    if extra is None:
        extra = {}

    # test existence of option
    try:
        opt_require = import_module("pkglts.option.%s.require" % name)
        opt_cfg = import_module("pkglts.option.%s.config" % name)
    except ImportError:
        raise KeyError("option '%s' does not exists" % name)

    # find other option requirements in repository
    for option_name in opt_require.option:
        if option_name not in pkg_cfg:
            print("need to install option '%s' first" % option_name)
            if (extra.get("install_option_dependencies", False) or
                    get_user_permission("install")):
                pkg_cfg = update_opt(option_name, pkg_cfg, extra)
            else:
                return pkg_cfg

    # find extra package requirements for setup
    msg = "this option requires some packages to setup"
    if not ensure_installed_packages(opt_require.setup, msg):
        print("option installation stopped")
        return pkg_cfg

    # execute main function to retrieve config options
    option_cfg = opt_cfg.main(pkg_cfg, extra)

    # write new pkg_info file
    if option_cfg is not None:
        pkg_cfg[name] = option_cfg

    try:  # TODO: proper developer doc to expose this feature
        opt_cfg.after(pkg_cfg)
    except AttributeError:
        pass

    # find extra package requirements for dvlpt
    msg = "this option requires additional packages for developers"
    ensure_installed_packages(opt_require.dvlpt, msg)

    return pkg_cfg


def clone_base_option_dir(src_dir, tgt_dir, pkg_cfg, handlers, overwrite_file):
    """ Clone src_dir into tgt_dir

    args:
     - src_dir (str): path to source directory
     - tgt_dir (str): path to target directory in which to copy files
     - pkg_cfg (dict of (str, dict)): package configuration parameters
     - handlers (dict of func): associate keys to handler functions
     - overwrite_files (dict of (str, bool)): whether to overwrite a specific
                                              path in case of conflict
    """
    error_files = []

    for src_name, is_dir in ls(src_dir):
        src_pth = src_dir + "/" + src_name
        tgt_name = replace(src_name, handlers, pkg_cfg)
        tgt_pth = tgt_dir + "/" + tgt_name
        # handle namespace
        if (is_dir and basename(src_dir) == 'src' and
                    src_name == tpl_src_name):
            namespace = pkg_cfg['base']['namespace']
            if namespace is not None:
                ns_pth = tgt_dir + "/" + namespace
                if not exists(ns_pth):
                    mkdir(ns_pth)

                init_namespace_dir(ns_pth)
                tgt_pth = ns_pth + "/" + tgt_name

        if is_dir:
            if tgt_name not in ("", "_") and not exists(tgt_pth):
                mkdir(tgt_pth)

            ef = clone_base_option_dir(src_pth, tgt_pth, pkg_cfg, handlers,
                                       overwrite_file)
            error_files.extend(ef)
        else:
            if (tgt_name.split(".")[0] != "_" and
                    tgt_name[-3:] not in ("pyc", "pyo")):
                if exists(tgt_pth):
                    if overwrite_file.get(tgt_pth, True):
                        src_cnt = get(src_pth)
                        with open(tgt_pth, 'r') as f:
                            tgt_cnt = f.read()

                        content = swap_divs(src_cnt, tgt_cnt,
                                            get_comment_marker(src_pth))
                        if content is None:
                            error_files.append(tgt_pth)
                        else:
                            write_file(tgt_pth, content)
                else:
                    content = get(src_pth)
                    write_file(tgt_pth, content)

    return error_files


def clone_base_option(option, pkg_cfg, handlers, target, overwrite_file):
    """ Copy all files in option repository to target

    Do not overwrite existing files, just ensure that
    a clone of option repository exists.

    args:
     - option (str): name of option
     - pkg_cfg (dict of (str, dict)): package configuration parameters
     - handlers (dict of func): associate keys to handler functions
     - target (str): path to copy files to
    """
    if (option, True) not in ls("pkglts_data/base"):
        return []  # nothing to do

    option_root = "pkglts_data/base/%s" % option

    return clone_base_option_dir(option_root, target, pkg_cfg, handlers,
                                 overwrite_file)


def clone_example(src_dir, tgt_dir, pkg_cfg, handlers):
    """ Clone an example directory into tgt_dir
    replacing text in files on the way.
    """
    for src_name, is_dir in ls(src_dir):
        src_pth = src_dir + "/" + src_name

        tgt_name = replace(src_name, handlers, pkg_cfg)
        tgt_pth = tgt_dir + "/" + tgt_name

        if is_dir:
            if tgt_name not in ("", "_") and not exists(tgt_pth):
                mkdir(tgt_pth)

            clone_example(src_pth, tgt_pth, pkg_cfg, handlers)
        else:
            if (tgt_name.split(".")[0] != "_" and
                    tgt_name[-3:] not in ("pyc", "pyo")):
                if exists(tgt_pth):
                    print("conflict '%s'" % tgt_name)
                else:
                    content = replace(get(src_pth), handlers, pkg_cfg)
                    write_file(tgt_pth, content)


def package_hash_keys(target):
    """ Walk all files in package and compute their hash key

    args:
     - pkg_cfg (dict of (str, dict)): package configuration parameters
     - target (str): path to read files from
    """
    hm = {}
    for root, dnames, fnames in walk(target):
        for name in tuple(dnames):
            if name.startswith("."):
                dnames.remove(name)
            elif "regenerate.no" in listdir(root + "/" + name):
                dnames.remove(name)

        for name in fnames:
            pth = (root + "/" + name).replace("\\", "/")
            hm[pth] = get_hash(pth)

    return hm


def regenerate_file(pth, pkg_cfg, handlers):
    """ Regenerate the content of a file, loading divs in
    pkglts_data.base if necessary.
    """
    with open(pth, 'r') as f:
        content = f.read()

    new_content = replace(content, handlers, pkg_cfg, get_comment_marker(pth))

    with open(pth, 'w') as f:
        f.write(new_content)


def regenerate_pkg(pkg_cfg, handlers, target, overwrite_file):
    """ Walk all files in package and replace content

    args:
     - pkg_cfg (dict of (str, dict)): package configuration parameters
     - handlers (dict of func): associate keys to handler functions
     - target (str): path to copy files to
     - overwrite_file (dict of (str, bool)): whether or not to overwrite
                                              a specific file
    """
    for name in listdir(target):
        pth = target + "/" + name
        if isdir(pth):
            # exclusion rule
            if name.startswith("."):
                pass
            elif "regenerate.no" in listdir(pth):
                pass
            else:
                # regenerate
                regenerate_pkg(pkg_cfg, handlers, pth, overwrite_file)
        else:
            if overwrite_file.get(pth, True):
                regenerate_file(pth, pkg_cfg, handlers)
