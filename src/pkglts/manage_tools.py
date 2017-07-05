""" Specific helper function for manage script
"""

from importlib import import_module
import logging
from os import listdir, mkdir
from os.path import basename, exists, isdir, splitext

from .config_management import ConfigSection, installed_options
from .hash_management import compute_hash, pth_as_key
from .install_env.load_front_end import get_install_front_end
from .local import init_namespace_dir
from .option_tools import get_user_permission
from .templating import render


logger = logging.getLogger(__name__)

tpl_src_name = "{" + "{ base.pkgname }" + "}"

non_bin_ext = ("", ".bat", ".cfg", ".in", ".ini", ".no", ".py", ".rst", ".sh",
               ".txt", ".yml", ".yaml")


def ensure_installed_packages(requirements, msg, env):
    """Ensure all packages in requirements are installed.

    If not, ask user permission to install them.

    Args:
        requirements (list of str): list of package names to install
                                   if needed
        msg (str): error message to print
        env (jinja2.Environment): current working environment

    Returns:
        (bool): whether all required packages are installed or not
    """
    ife_name = env.globals["_pkglts"].install_front_end
    req = [dep.name for dep in requirements
           if dep.package_manager is None or dep.package_manager == ife_name]
    ife = get_install_front_end(ife_name)
    to_install = set(req) - set(ife.installed_packages())
    if len(to_install) > 0:
        print(msg)
        logger.warning("missing packages: " + ", ".join(to_install))
        for name in to_install:
            ife.install(name)
            logger.info("install %s", name)

    return True


def check_option_parameters(name, env):
    """Check that the parameters associated to an option are valid.

    Try to import Check function in option dir.

    Args:
        name (str): option name
        env (jinja2.Environment): current working environment
    """
    try:
        opt_cfg = import_module("pkglts.option.%s.config" % name)
        try:
            return opt_cfg.check(env)
        except AttributeError:
            return []
    except ImportError:
        return []


def update_opt(name, env):
    """Update an option of this package.

    Notes: If the option does not exists yet, add it first.
           See the list of available option online

    Args:
        name (str): name of option to add
        env (jinja2.Environment): current working environment
    """
    logger.info("update option %s", name)

    # test existence of option
    try:
        opt_cfg = import_module("pkglts.option.%s.config" % name)
    except ImportError:
        raise KeyError("option '%s' does not exists" % name)

    # find other option requirements in repository
    for dep in opt_cfg.require('option', env):
        option_name = dep.name
        if option_name not in installed_options(env):
            print("need to install option '%s' first" % option_name)
            if (env.globals["_pkglts"].auto_install or
                    get_user_permission("install")):
                env = update_opt(option_name, env)
            else:
                return env

    # find extra package requirements for setup
    msg = "this option requires some packages to setup"
    if not ensure_installed_packages(opt_cfg.require('setup', env), msg, env):
        print("option installation stopped")
        return env

    # find parameters required by option config
    try:
        params = opt_cfg.parameters
    except AttributeError:
        params = []

    option_cfg = ConfigSection()
    prev_cfg = env.globals.get(name, {})
    for key, default in params:
        option_cfg.add_param(key, getattr(prev_cfg, key, default))

    # write new pkg_info file
    env.globals[name] = option_cfg

    try:  # TODO: proper developer doc to expose this feature
        opt_cfg.after(env)
    except AttributeError:
        pass

    # find extra package requirements for dvlpt
    msg = "this option requires additional packages for developers"
    ensure_installed_packages(opt_cfg.require('dvlpt', env), msg, env)

    return env


def regenerate_dir(src_dir, tgt_dir, env, overwrite_file):
    """Walk all files in src_dir and create/update them on tgt_dir

    Args:
        src_dir (str): path to reference files
        tgt_dir (str): path to target where files will be written
        env (jinja2.Environment): current working environment
        overwrite_file (dict of str, bool): whether or not to overwrite some
                             files

    Returns:
        (dict of str, map): hash key of preserved sections
    """
    hm = {}

    for src_name in listdir(src_dir):
        src_pth = src_dir + "/" + src_name
        tgt_name = env.from_string(src_name).render()
        if tgt_name.endswith(".tpl"):
            tgt_name = tgt_name[:-4]

        tgt_pth = tgt_dir + "/" + tgt_name
        # handle namespace
        if (isdir(src_pth) and basename(src_dir) == 'src' and
                    src_name == tpl_src_name):
            namespace = env.globals['base'].namespace
            if namespace is not None:
                ns_pth = tgt_dir + "/" + namespace
                if not exists(ns_pth):
                    mkdir(ns_pth)

                init_namespace_dir(ns_pth, env)
                tgt_pth = ns_pth + "/" + tgt_name

        if isdir(src_pth):
            if tgt_name not in ("", "_") and not exists(tgt_pth):
                mkdir(tgt_pth)

            sub_hm = regenerate_dir(src_pth, tgt_pth, env, overwrite_file)
            hm.update(sub_hm)
        else:
            kp = pth_as_key(tgt_pth)
            if overwrite_file.get(kp, True):
                fname, ext = splitext(tgt_name)
                if ext in non_bin_ext:
                    blocks = render(env, src_pth, tgt_pth)
                    hm[kp] = dict((bid, compute_hash(cnt)) for bid, cnt in blocks)
                else:  # binary file
                    if exists(tgt_pth):
                        print("overwrite? %s" % tgt_pth)
                    else:
                        with open(src_pth, 'rb') as fr:
                            content = fr.read()
                        with open(tgt_pth, 'wb') as fw:
                            fw.write(content)

    return hm
