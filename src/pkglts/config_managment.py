from importlib import import_module
from jinja2 import Environment, StrictUndefined, UndefinedError
import json
import logging
from os.path import join as pj

from .config import pkglts_dir, pkg_cfg_file

try:
    string_type = basestring
except NameError:
    string_type = str

current_pkg_cfg_version = 2

logger = logging.getLogger(__name__)

default_cfg = dict(_pkglts=dict(use_prompts=False,
                                auto_install=True,
                                install_front_end='stdout',
                                version=current_pkg_cfg_version))


class FormattedString(str):
    """Small class to hold both formatted string and its template
    """
    pass


class ConfigSection(object):
    """Small class to gather config keys
    """
    def __init__(self):
        self._params = []

    def add_param(self, key, val):
        """Add a new attribute to this section

        Args:
            key (str): python valid identifier
            val (any):

        Returns:
            (None)
        """
        self._params.append(key)
        setattr(self, key, val)

    def items(self):
        """Iterates on couple key, values stored as attributes

        Returns:
            (iter of str: any)
        """
        for key in self._params:
            yield key, getattr(self, key)


def create_env(pkg_cfg):
    """Create a jinja2.Environment from a package configuration

    Notes: do not load option handlers

    Args:
        pkg_cfg (dict of str: any): package configuration

    Returns:
        (jinja2.Environment)
    """
    env = Environment(undefined=StrictUndefined)
    env.keep_trailing_newline = True

    to_eval = []
    for opt_name, cfg in pkg_cfg.items():
        env.globals[opt_name] = ConfigSection()
        for key, param in cfg.items():
            if isinstance(param, string_type):
                to_eval.append((opt_name, key, param))
            else:
                env.globals[opt_name].add_param(key, param)

    nb_iter_max = len(to_eval) ** 2
    cur_iter = 0
    while len(to_eval) > 0 and cur_iter < nb_iter_max:
        cur_iter += 1
        opt_name, key, param = to_eval.pop(0)
        try:
            txt = env.from_string(param).render()
            if txt != param:
                txt = FormattedString(txt)
                txt.template = param
            env.globals[opt_name].add_param(key, txt)
        except UndefinedError:
            to_eval.append((opt_name, key, param))

    if len(to_eval) > 0:
        msg = "unable to fully render config\n"
        for item in to_eval:
            msg += "%s:%s '%s'\n" % item
        raise UserWarning(msg)

    # add global filters and test
    env.globals['today'] = lambda: "TODAY"  # TODO

    def is_available(opt_param):
        return opt_param in installed_options(env)

    env.tests['available'] = is_available

    return env


def pkg_env(pkg_cfg):
    """Create a jinja2.Environment from a package configuration

    Args:
        pkg_cfg (dict of str: any): package configuration

    Returns:
        (jinja2.Environment)
    """
    env = create_env(pkg_cfg)

    # load option specific handlers
    for name in pkg_cfg:
        if not name.startswith("_"):
            try:
                opt_handlers = import_module("pkglts.option.%s.handlers" % name)
                if not hasattr(opt_handlers, "environment_extensions"):
                    logger.debug("option %s do not define any extension" % name)
                else:
                    extensions = opt_handlers.environment_extensions(env)
                    for k, v in extensions.items():
                        setattr(env.globals[name], k, v)
            except ImportError:
                raise KeyError("option '%s' does not exists" % name)

    return env


def get_pkg_config(rep="."):
    """Read pkg_cfg file associated to this package.

    Args:
        rep (str): directory to search for info

    Returns:
        (jinja2.Environment): env.globals initialized with pkg_config
    """
    with open(pj(rep, pkglts_dir, pkg_cfg_file), 'r') as f:
        pkg_cfg = json.load(f)

    # update version of pkg_config
    file_version = pkg_cfg['_pkglts'].get('version', 0)
    for i in range(file_version, current_pkg_cfg_version):
        upgrade_pkg_cfg_version(pkg_cfg, i)

    # create jinja2 Environment
    return pkg_env(pkg_cfg)


def write_pkg_config(env, rep="."):
    """Store config associated to this package on disk.

    Args:
        env (jinja2.Environment): current working environment
        rep (str): directory to search for info

    Returns:
        None
    """
    logger.info("write package config")
    pkg_cfg = {}
    for opt_name, cfg in env.globals.items():
        if isinstance(cfg, ConfigSection):
            pkg_cfg[opt_name] = {}
            for key, val in cfg.items():
                if isinstance(val, FormattedString):
                    val = val.template
                pkg_cfg[opt_name][key] = val

    with open(pj(rep, pkglts_dir, pkg_cfg_file), 'w') as f:
        json.dump(pkg_cfg, f, sort_keys=True, indent=4)


def upgrade_pkg_cfg_version(pkg_cfg, version):
    """Upgrade the version of pkg_cfg file from version to version +1

    Args:
        pkg_cfg (dict of str: any): package configuration
        version (int): current version of file

    Returns:
        (dict of str: any): a reference to an updated pkg_cfg
    """
    # if version == 0:
    #     pkg_cfg['_pkglts']['version'] = 1
    # elif version == 1:
    #     try:
    #         sphinx_cfg = pkg_cfg['sphinx']
    #         sphinx_cfg['autodoc-dvlpt'] = sphinx_cfg.get('autodoc-dvlpt', True)
    #     except KeyError:
    #         pass
    #
    #     pkg_cfg['_pkglts']['version'] = 2

    return pkg_cfg


def installed_options(env):
    """List all installed options according to current environment

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (iter of str)
    """
    for key, cfg in env.globals.items():
        if isinstance(cfg, ConfigSection) and not key.startswith("_"):
            yield key
