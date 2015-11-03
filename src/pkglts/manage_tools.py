""" Specific helper function for manage script
"""

from importlib import import_module
from os.path import exists
import pip

from .file_management import make_dir, user_modified, write_file
from .local import init_namespace_dir
from .option_tools import get_user_permission
from .rmtfile import get, ls
from .templating import get_comment_marker, replace


def check_tempering(cur_src_pth, cur_dst_pth, handlers, pkg_cfg, tf):
    """ Parse cur_src_pth assumed to be a directory
    in repository and check all files in it to detect
    tempering by user.

    Function called recursively on sub directories

    Does not make any test on the existence of cur_dst_pth

    args:
     - cur_src_pth (str): current pth to look into
     - cur_dst_pth (str): mirror of cur_src_pth on destination
     - handlers (dict of func): associate keys to handler functions
     - pkg_cfg (dict of (str: dict)): more information to pass to handlers
     - tf (list of str): list of tempered files to update, side effect
    """
    items = ls(cur_src_pth)
    for name, is_dir_type in items:
        if is_dir_type:
            new_name = replace(name, handlers, pkg_cfg)
            if new_name not in ("", "_"):
                dst_dir = cur_dst_pth
                # handling of namespace
                if name == "{{base rm, {{key, base.pkgname}}}}":
                    if 'base' in pkg_cfg:
                        # check for namespace directory
                        namespace = pkg_cfg['base']['namespace']
                        if namespace is not None:
                            dst_dir += "/" + namespace
                            pth = dst_dir + "/__init__.py"
                            if exists(pth) and user_modified(pth,
                                                             pkg_cfg['hash']):
                                tf.append(pth)

                dst_dir += "/" + new_name
                if not exists(dst_dir) and dst_dir in pkg_cfg['hash']:
                    # print("Directory '%s' has been removed" % dst_dir)
                    pass
                else:
                    check_tempering(cur_src_pth + "/" + name,
                                    dst_dir,
                                    handlers,
                                    pkg_cfg,
                                    tf)
        else:
            new_name = replace(name, handlers, pkg_cfg)
            if new_name.split(".")[0] != "_":
                pth = cur_dst_pth + "/" + new_name
                if exists(pth) and user_modified(pth, pkg_cfg['hash']):
                    # print("user modified file: %s" % pth)
                    tf.append(pth)


def regenerate_dir(cur_src_pth, cur_dst_pth, handlers, pkg_cfg,
                   store_hash=True):
    """ Parse cur_src_pth assumed to be a directory
    in repository and regenerate all files in it
    copy regenerated files in cur_dst_pth.

    Function called recursively on sub directories

    Does not make any test on the existence of cur_dst_pth

    args:
     - cur_src_pth (str): current pth to look into
     - cur_dst_pth (str): mirror of cur_src_pth on destination
     - handlers (dict of func): associate keys to handler functions
     - pkg_cfg (dict of (str: dict)): more information to pass to handlers
     - store_hash (bool): default True, whether to store hash associated
                          with newly created files or not
    """
    if store_hash:
        hashmap = pkg_cfg['hash']
    else:
        hashmap = None

    overwrite = pkg_cfg.get('_session', {}).get('overwrite', {})

    items = ls(cur_src_pth)
    for name, is_dir_type in items:
        if is_dir_type:
            new_name = replace(name, handlers, pkg_cfg)
            if new_name not in ("", "_"):  # TODO: Bof when removing one option
                # handling of namespace
                dst_dir = cur_dst_pth
                if name == "{{base rm, {{key, base.pkgname}}}}":
                    if 'base' in pkg_cfg:
                        # check for namespace directory
                        namespace = pkg_cfg['base']['namespace']
                        if namespace is not None:
                            dst_dir += "/" + namespace
                            if not exists(dst_dir):
                                make_dir(dst_dir, hashmap)
                                init_namespace_dir(dst_dir, hashmap)

                dst_dir += "/" + new_name
                if not exists(dst_dir):
                    make_dir(dst_dir, hashmap)

                regenerate_dir(cur_src_pth + "/" + name, dst_dir,
                               handlers, pkg_cfg, store_hash)
        else:
            new_name = replace(name, handlers, pkg_cfg)
            if (new_name.split(".")[0] != "_" and
               new_name[-3:] not in ("pyc", "pyo")):
                # TODO: Bof when removing one option
                new_pth = cur_dst_pth + "/" + new_name
                if new_pth not in overwrite or overwrite[new_pth]:
                    src_content = get(cur_src_pth + "/" + name)
                    new_src_content = replace(src_content, handlers, pkg_cfg,
                                              get_comment_marker(new_name))
                    # overwrite file without any warning
                    write_file(new_pth, new_src_content, hashmap)


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
    installed = set(p.project_name for p in pip.get_installed_distributions())
    to_install = [n for n in opt_require.setup if n not in installed]
    if len(to_install) > 0:
        print("this option requires additional packages to setup:")
        print(", ".join(to_install))
        if get_user_permission("install"):
            pip.main(['install'] + to_install)
        else:
            return pkg_cfg

    # execute main function to retrieve config options
    option_cfg = opt_cfg.main(pkg_cfg, extra)

    # write new pkg_info file
    if option_cfg is not None:
        pkg_cfg[name] = option_cfg

    try:  # TODO: proper doc to expose this feature
        opt_cfg.after(pkg_cfg)
    except AttributeError:
        pass

    return pkg_cfg
