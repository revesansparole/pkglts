from pkglts.config_management import installed_options
from pkglts.dependency import Dependency
from pkglts.option_tools import available_options


def requirements(env, requirement_name):
    """Check all requirements for installed options.

    Args:
        env (jinja2.Environment):
        requirement_name (str): type of requirement 'install', 'dvlpt'

    Returns:
        (list of str): list of required packages names
    """
    reqs = {}
    for name in installed_options(env):
        try:
            opt = available_options[name]
            for dep in opt.require(requirement_name, env):
                reqs[dep.name] = dep
        except ImportError:
            raise KeyError("option '%s' does not exists" % name)

    return [reqs[name] for name in sorted(reqs)]


def pkg_url(env):
    try:
        url = env.globals['base'].url
        if url is not None:
            return url
    except KeyError:
        pass

    try:
        url = env.globals['github'].url
        if url is not None:
            return url
    except KeyError:
        pass

    try:
        url = env.globals['pypi'].url
        if url is not None:
            return url
    except KeyError:
        pass

    try:
        url = env.globals['readthedocs'].url
        if url is not None:
            return url
    except KeyError:
        pass

    return ""


def environment_extensions(env):
    """Add more functionality to an environment.

    Args:
        env (jinja2.Environment):

    Returns:
        dict of str: any
    """
    req_install = requirements(env, 'install')
    for dep in env.globals['pysetup'].require:
        req_install.append(Dependency(**dep))

    req_dvlpt = requirements(env, 'dvlpt')

    def req(name):
        if name == 'install':
            return req_install
        elif name == 'dvlpt':
            return req_dvlpt
        else:
            raise UserWarning("WTF")

    return {"pkg_url": pkg_url(env),
            "requirements": req}
