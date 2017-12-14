"""
Main config object and functions to manipulate it.
"""
from datetime import date
from jinja2 import Environment, StrictUndefined, UndefinedError
import json
import logging
from os.path import join as pj

from .config import pkglts_dir, pkg_cfg_file
from .option_tools import available_options, find_available_options
from .option.git.config import update_parameters as git_update_parameters
from .option.pypi.config import update_parameters as pypi_update_parameters

try:
    string_type = basestring
except NameError:
    string_type = str

current_pkg_cfg_version = 11

logger = logging.getLogger(__name__)

default_cfg = dict(_pkglts=dict(use_prompts=False,
                                auto_install=True,
                                install_front_end='stdout',
                                version=current_pkg_cfg_version))

find_available_options()


class ConfigSection(object):
    """Small class to allow accessing parameters using the dot
    method instead of ['param_name'] method
    """
    pass


class Config(dict):
    """Object used to store both a templated version of the config as a dict interface
    its resolution and a jinja2 environment that reflect the config.
    """

    def __init__(self, *args, **kwds):
        dict.__init__(self)
        self._tpl = dict(*args, **kwds)

        # initialise associated Jinja2 environment
        self._env = Environment(undefined=StrictUndefined)
        self._env.keep_trailing_newline = True

        # add global filters and test
        self._env.globals['today'] = lambda: date.today().isoformat()

        self.add_test('available', self._is_available)

        # resolve
        self.resolve()

    def template(self):
        return self._tpl

    def add_test(self, name, func):
        """Add a new test in jinja2 environment.

        Args:
            name (str): name of test (must be unique)
            func (callable): function use for test

        Returns:
            None
        """
        self._env.tests[name] = func

    def _is_available(self, opt_name):
        return opt_name in self

    def _add_param(self, opt_name, param_name, param_value):
        """Add a new parameter value in the config

        Args:
            opt_name (str): Option name
            param_name (str): parameter name
            param_value (any): parameter value

        Returns:
            None
        """
        self[opt_name][param_name] = param_value
        setattr(self._env.globals[opt_name], param_name, param_value)

    def resolve(self):
        """Try to resolve all templated items.

        Returns:
            None
        """
        to_eval = []
        for opt_name, cfg in self._tpl.items():
            self[opt_name] = {}
            self._env.globals[opt_name] = ConfigSection()
            for key, param in cfg.items():
                if isinstance(param, string_type):
                    to_eval.append((opt_name, key, param))
                else:
                    self._add_param(opt_name, key, param)

        nb_iter_max = len(to_eval) ** 2
        cur_iter = 0
        while len(to_eval) > 0 and cur_iter < nb_iter_max:
            cur_iter += 1
            opt_name, key, param = to_eval.pop(0)
            try:
                txt = self.render(param)
                self._add_param(opt_name, key, txt)
            except UndefinedError:
                to_eval.append((opt_name, key, param))

        if len(to_eval) > 0:
            msg = "unable to fully render config\n"
            for item in to_eval:
                msg += "%s:%s '%s'\n" % item
            raise UserWarning(msg)

    def load_extra(self):
        """load option specific handlers.

        Returns:
            None
        """
        for name in self:
            if not name.startswith("_"):
                try:
                    opt = available_options[name]
                    for k, v in opt.environment_extensions(self).items():
                        setattr(self._env.globals[name], k, v)
                except KeyError:
                    raise KeyError("option '%s' does not exists" % name)

    def installed_options(self):
        """List all installed options.

        Returns:
            (iter of str)
        """
        for key in self:
            if not key.startswith("_"):
                yield key

    def render(self, txt):
        """Use items in config to render text

        Args:
            txt (str): templated text to render

        Returns:
            (str): same text where all templated parts have been replaced
                   by their values.
        """
        return self._env.from_string(txt).render()


def get_pkg_config(rep="."):
    """Read pkg_cfg file associated to this package.

    Args:
        rep (str): directory to search for info

    Returns:
        (Config): Config initialized with pkg_config
    """
    with open(pj(rep, pkglts_dir, pkg_cfg_file), 'r') as f:
        pkg_cfg = json.load(f)

    # update version of pkg_config
    file_version = pkg_cfg['_pkglts'].get('version', 0)
    for i in range(file_version, current_pkg_cfg_version):
        upgrade_pkg_cfg_version(pkg_cfg, i)

    # create Config object
    cfg = Config(pkg_cfg)
    cfg.load_extra()

    # write back config if version has been updated
    if file_version < current_pkg_cfg_version:
        write_pkg_config(cfg, rep)

    return cfg


def write_pkg_config(cfg, rep="."):
    """Store config associated to this package on disk.

    Args:
        cfg (Config): current working config
        rep (str): directory to search for info

    Returns:
        None
    """
    logger.info("write package config")
    pkg_cfg = dict(cfg.template())

    with open(pj(rep, pkglts_dir, pkg_cfg_file), 'w') as f:
        json.dump(pkg_cfg, f, sort_keys=True, indent=2)


def upgrade_pkg_cfg_version(pkg_cfg, version):
    """Upgrade the version of pkg_cfg file from version to version +1

    Args:
        pkg_cfg (dict of str, any): package configuration
        version (int): current version of file

    Returns:
        (dict of str: any): a reference to an updated pkg_cfg
    """
    if version == 0:
        pkg_cfg['_pkglts']['version'] = 1
    elif version == 1:
        pkg_cfg['_pkglts']['version'] = 2
    elif version == 2:
        pkg_cfg['_pkglts']['version'] = 3
        if 'pysetup' in pkg_cfg:
            section = pkg_cfg['pysetup']
            section['require'] = section.get('require', [])
    elif version == 3:
        pkg_cfg['_pkglts']['version'] = 4
        if 'test' in pkg_cfg:
            section = pkg_cfg['test']
            section['suite_name'] = section.get('suite_name', "pytest")
    elif version == 4:
        pkg_cfg['_pkglts']['version'] = 5
        if 'base' in pkg_cfg:
            section = pkg_cfg['base']
            section['namespace_method'] = section.get('namespace_method', "pkg_util")
    elif version == 5:
        pkg_cfg['_pkglts']['version'] = 6
        if 'pysetup' in pkg_cfg:
            section = pkg_cfg['pysetup']
            deps = []
            for pkg_mng, name in section.get('require', []):
                if pkg_mng == 'none':
                    deps.append(dict(name=name))
                else:
                    deps.append(dict(name=name, pkg_mng=pkg_mng))
            section['require'] = deps
    elif version == 6:
        pkg_cfg['_pkglts']['version'] = 7
        if 'sphinx' in pkg_cfg:
            section = pkg_cfg['sphinx']
            section['build_dir'] = section.get('build_dir', "build/sphinx")
    elif version == 7:
        pkg_cfg['_pkglts']['version'] = 8
        if 'doc' in pkg_cfg:
            section = pkg_cfg['doc']
            section['fmt'] = section.get('fmt', 'rst')
    elif version == 8:
        pkg_cfg['_pkglts']['version'] = 9
        if 'github' in pkg_cfg or 'gitlab' in pkg_cfg:
            print("#" * 20 + "\n" * 2)
            print("please remove '.gitignore file and regenerate package")
            print("\n" * 2 + "#" * 20)
            git_update_parameters(pkg_cfg)
    elif version == 9:
        pkg_cfg['_pkglts']['version'] = 10
        if 'pypi' in pkg_cfg:
            print("#" * 20 + "\n" * 2)
            print("please remove '.pypirc file and regenerate package")
            print("\n" * 2 + "#" * 20)
            # save section
            mem = dict(pkg_cfg["pypi"])
            # get newly defined list of servers
            pypi_update_parameters(pkg_cfg)
            servers = dict(pkg_cfg["pypi"]["servers"])
            # update option
            pkg_cfg["pypi"] = mem
            pkg_cfg["pypi"]["servers"] = pkg_cfg["pypi"].get("servers", {})
            pkg_cfg["pypi"]["servers"].update(servers)
    elif version == 10:
        pkg_cfg['_pkglts']['version'] = 11
        if 'data' in pkg_cfg:
            section = pkg_cfg['data']
            section['filetype'] = section.get('filetype', [".json", ".ini"])
            section['use_ext_dir'] = section.get('use_ext_dir', False)

    return pkg_cfg
