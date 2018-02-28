from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.option_tools import available_options


class OptionPysetup(Option):
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

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['base', 'test', 'doc', 'license', 'version']
            return [Dependency(name) for name in options]

        return []

    def environment_extensions(self, cfg):
        req_install = requirements(cfg, 'install')
        req_dvlpt = requirements(cfg, 'dvlpt')

        def req(name):
            """For internal use only."""
            if name == 'install':
                return req_install
            elif name == 'dvlpt':
                return req_dvlpt
            else:
                raise UserWarning("WTF")

        cfg.add_test('is_pip_dep', Dependency.is_pip)

        return {"pkg_url": pkg_url(cfg),
                "requirements": req}


def requirements(cfg, requirement_name):
    """Check all requirements for installed options.

    Args:
        cfg (Config):  current package configuration
        requirement_name (str): type of requirement 'install', 'dvlpt'

    Returns:
        (list of str): list of required packages names
    """
    reqs = {}
    for name in cfg.installed_options():
        try:
            opt = available_options[name]
            for dep in opt.require(requirement_name, cfg):
                reqs[dep.name] = dep
        except KeyError:
            raise KeyError("option '%s' does not exists" % name)

    if requirement_name == 'install':
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
