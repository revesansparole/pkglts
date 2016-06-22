from importlib import import_module

from pkglts.config_managment import installed_options


def requirements(pkg_cfg, requirement_name):
    """ Check all requirements for installed options

    args:
     - pkg_cfg (dict of (str, dict)): option_name, options
     - requirement_name (str): type of requirement 'install', 'dvlpt'

    return:
     - (str): one requirement per line
    """
    reqs = set()
    for name in installed_options(pkg_cfg):
        try:
            opt_req = import_module("pkglts.option.%s.require" % name)
            reqs.update(getattr(opt_req, requirement_name))
        except ImportError:
            raise KeyError("option '%s' does not exists" % name)

    reqs_str = "\n".join(reqs)
    return "\n" + reqs_str + "\n"


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
    req_install = ['install1', 'install2']
    req_dvlpt = ['dvlpt1', 'dvlpt2']

    def req(name):
        if name == 'install':
            return req_install
        elif name == 'dvlpt':
            return req_dvlpt
        else:
            raise UserWarning("WTF")

    return {"pkg_url": pkg_url(env),
            "requirements": req}
