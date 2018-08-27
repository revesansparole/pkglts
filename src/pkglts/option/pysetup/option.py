from os.path import dirname
from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.option_tools import available_options
from pkglts.version import __version__

from . import find_requirements


class OptionPysetup(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            intended_versions=["36"],
            require=[]
        )
        cfg['pysetup'] = sec

    def check(self, cfg):
        invalids = []
        intended_versions = cfg['pysetup']['intended_versions']

        if not intended_versions:
            invalids.append("pysetup.intended_versions")

        req = cfg['pysetup']['require']

        valid_methods = (None, "pip", "conda", "git")
        if any(dep.get('pkg_mng') not in valid_methods for dep in req):
            invalids.append("pysetup.require")

        return invalids

    def require_option(self):
        return ['base', 'test', 'doc', 'license', 'version']

    def tools(self, cfg):
        del cfg
        yield find_requirements.parser_find_reqs

    def environment_extensions(self, cfg):
        reqs = requirements(cfg)

        def req(intent):
            """For internal use only."""
            return [r for r in reqs if r.intent == intent]

        def conda_reqs(intents):
            return fmt_conda_reqs(reqs, intents)

        def pip_reqs(intents):
            return fmt_pip_reqs(reqs, intents)

        cfg.add_test('is_pip_dep', Dependency.is_pip)

        return {"pkg_url": pkg_url(cfg),
                "requirements": req,
                "conda_reqs": conda_reqs,
                "pip_reqs": pip_reqs}


def requirements(cfg):
    """Check all requirements for installed options.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (list): list of required packages
    """
    reqs = {}
    for name in cfg.installed_options():
        try:
            opt = available_options[name]
            for dep in opt.require(cfg):
                reqs[dep.name] = dep
        except KeyError:
            raise KeyError("option '%s' does not exists" % name)

    for dep_def in cfg['pysetup']['require']:
        dep = Dependency(**dep_def)
        reqs[dep.name] = dep

    return [reqs[name] for name in sorted(reqs)]


def pkg_url(cfg):
    """Extract a valid url from all config sections.

    Args:
        cfg (Config):  current package configuration

    Returns:
        (str): a valid url for the package
    """
    try:
        url = cfg['base']['url']
        if url is not None:
            return url
    except KeyError:
        pass

    try:
        url = cfg['github']['url']
        if url is not None:
            return url
    except KeyError:
        pass

    try:
        url = cfg['gitlab']['url']
        if url is not None:
            return url
    except KeyError:
        pass

    # try:
    #     url = cfg['pypi']['url']
    #     if url is not None:
    #         return url
    # except KeyError:
    #     pass

    # try:
    #     url = cfg['readthedocs']['url']
    #     if url is not None:
    #         return url
    # except KeyError:
    #     pass

    return ""


def fmt_conda_reqs(reqs, intents):
    """Produce conda cmd line to install list of requirements.

    Args:
        reqs (list of Dependency): list of requirements objects
        intents (list of str): list of intents for deps

    Returns:
        (str)
    """
    reqs = [r for r in reqs if r.is_conda(strict=False) and r.intent in intents]
    if len(reqs) == 0:
        return ""

    cmd = "conda install"
    for channel in set(r.channel for r in reqs) - {None}:
        cmd += " -c %s" % channel

    for name in sorted(r.conda_full_name() for r in reqs):
        cmd += " %s" % name

    return cmd


def fmt_pip_reqs(reqs, intents):
    """Produce pip cmd line to install list of requirements.

    Args:
        reqs (list of Dependency): list of requirements objects
        intents (list of str): list of intents for deps

    Returns:
        (str)
    """
    reqs = [r for r in reqs if r.is_pip(strict=True) and r.intent in intents]
    if len(reqs) == 0:
        return ""

    cmd = "pip install"

    for name in sorted(r.pip_full_name() for r in reqs):
        cmd += " %s" % name

    return cmd
