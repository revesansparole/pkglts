from importlib import import_module
import json

from pkglts.local import installed_options


def requirements(txt, env):
    """ Check all requirements for installed options
    and add them to setup.py
    """
    reqs = set()
    for name in installed_options(env):
        try:
            opt_req = import_module("pkglts.option.%s.require" % name)
            reqs.update(opt_req.install)
        except ImportError:
            raise KeyError("option '%s' does not exists" % name)

    reqs_str = "\n".join(reqs)
    return reqs_str


def get_url(txt, pkg_cfg):
    try:
        url = pkg_cfg['base']['url']
        if url is not None:
            return url
    except KeyError:
        pass

    try:
        url = pkg_cfg['github']['url']
        if url is not None:
            return url
    except KeyError:
        pass

    try:
        url = pkg_cfg['pypi']['url']
        if url is not None:
            return url
    except KeyError:
        pass

    try:
        url = pkg_cfg['readthedocs']['url']
        if url is not None:
            return url
    except KeyError:
        pass

    return ""


def get_extra(txt, env):
    """ Fetch extra entry points
    """
    try:
        with open("entry_points.json", 'r') as f:
            ep_def = json.load(f)
            items = ["    entry_points={"]
            for gr, eps in ep_def.items():
                items.append("        '%s': [" % gr)
                for ep in eps:
                    items.append("            '%s'," % ep)
                items.append("        ],")

            items.append("    },\n")
            return "\n".join(items)
    except IOError:
        pass

    return txt


mapping = {"requirements": requirements,
           "pkg_url": get_url,
           "pydist.extra": get_extra}
