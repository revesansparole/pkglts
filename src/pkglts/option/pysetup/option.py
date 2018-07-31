from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.option_tools import available_options
from pkglts.version import __version__


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

    def environment_extensions(self, cfg):
        reqs = requirements(cfg)

        def req(intent):
            """For internal use only."""
            return [r for r in reqs if r.intent == intent]

        cfg.add_test('is_pip_dep', Dependency.is_pip)

        return {"pkg_url": pkg_url(cfg),
                "requirements": req}


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
