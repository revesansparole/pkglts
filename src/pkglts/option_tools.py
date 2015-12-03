""" Some helpers for options
"""
try:
    loc_input = raw_input
except NameError:
    loc_input = input


def get_user_permission(action_name, default_true=True):
    if default_true:
        return loc_input("%s [y], n?" % action_name) in ("", "y")
    else:
        return loc_input("%s y, [n]?" % action_name) == "y"


def get_key(key, env):
    """ Fetch a specific key in env
    """
    try:
        elms = key.split(".")
        d = env
        for k in elms:
            d = d[k]

        return d
    except KeyError:
        return None


def _ask_single_arg(name, default):
    # prompt user for value
    msg = name
    if default is None:
        msg += ":"
        val = ""
    else:
        val = str(default)
        msg += " [%s]:" % val

    ans = loc_input(msg)
    if ans == "":
        return val
    else:
        return ans


def ask_arg(name, pkg_cfg=None, default=None, extra=None):
    """ Prompt the user for the value of some argument

    If user returns nothing then default will be returned

    If pkg_cfg is provided, the function will attempt to
    find a proper default in it.

    If extra is provided, the function will attempt to
    find a value in it and return it without prompting
    the user.

    If default is a list of elements, even empty, the function
    will return a list of answers.

    args:
     - name (str): name of argument. Can be in the form of
                   'option.arg'.
     - pkg_cfg (dict of (str, any)): place to look for defaults
     - default (any): default to use as a last resort
     - extra (dict of (str, any)): place to look for values

    return:
     - (str): value of argument either from prompt or from default
    """
    if extra is None:
        extra = {}

    # try to find value in extra
    if name in extra:
        return extra[name]

    key = name.split(".")[-1]
    if key in extra:
        return extra[key]

    if pkg_cfg is None:
        pkg_cfg = {}

    if isinstance(default, (list, tuple)):
        # ask multiple args
        val = get_key(name, pkg_cfg)
        if val is None:
            val = default

        if not isinstance(val, (list, tuple)):
            msg = "bad value in pkg_cfg, expected list for %s" % name
            raise UserWarning(msg)

        i = 0
        items = []
        res = "txt"
        while res != "":
            if i < len(val):
                loc_val = val[i]
            else:
                loc_val = ""
            res = _ask_single_arg(name, loc_val)
            if res != "":
                items.append(res)
                i += 1

        return items
    else:
        val = get_key(name, pkg_cfg)
        if val is None:
            val = default
        return _ask_single_arg(name, val)


def edit_option_parameters(name, pkg_cfg):
    """Prompt user for parameters associated with option.

    args:
     - name (str): option name
     - pkg_cfg (dict of (str, dict)): package configuration file

    return:
     - pkg_cfg (dict of (str, dict)): new package configuration
    """
    pkg_cfg = dict(pkg_cfg)
    cfg = pkg_cfg[name]
    for key, val in tuple(cfg.items()):
        nval = _ask_single_arg(key, val)  # TODO problem with param type
        raise NotImplementedError
