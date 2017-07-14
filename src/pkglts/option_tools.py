""" Some helpers for options
"""
import logging
import pkg_resources

logger = logging.getLogger(__name__)

available_options = {}

try:
    loc_input = raw_input
except NameError:
    loc_input = input


class Option(object):
    """Base class to store information associated with an option
    """

    def __init__(self):
        self._name = None
        self._update_parameters = None
        self._check = None
        self._require = None
        self._environment_extensions = None
        self._regenerate = None

    def from_entry_point(self, ep):
        self._name, func_name = ep.name.split(".")
        if func_name == "update_parameters":
            self._update_parameters = ep
        elif func_name == "check":
            self._check = ep
        elif func_name == "require":
            self._require = ep
        elif func_name == "environment_extensions":
            self._environment_extensions = ep
        elif func_name == "regenerate":
            self._regenerate = ep
        else:
            # silently ignore other type of entry points
            logger.error("unknown entry point attribute: '{}'".format(func_name))

    def update_parameters(self, cfg):
        if self._update_parameters is None:
            cfg[self._name] = {}
            return

        if isinstance(self._update_parameters, pkg_resources.EntryPoint):
            self._update_parameters = self._update_parameters.load()

        return self._update_parameters(cfg)

    def check(self, *args, **kwds):
        if self._check is None:
            return []

        if isinstance(self._check, pkg_resources.EntryPoint):
            self._check = self._check.load()

        return self._check(*args, **kwds)

    def require(self, *args, **kwds):
        if self._require is None:
            return []

        if isinstance(self._require, pkg_resources.EntryPoint):
            self._require = self._require.load()

        return self._require(*args, **kwds)

    def environment_extensions(self, *args, **kwds):
        if self._environment_extensions is None:
            return {}

        if isinstance(self._environment_extensions, pkg_resources.EntryPoint):
            self._environment_extensions = self._environment_extensions.load()

        return self._environment_extensions(*args, **kwds)

    def regenerate(self, *args, **kwds):
        if self._regenerate is None:
            return None

        if isinstance(self._regenerate, pkg_resources.EntryPoint):
            self._regenerate = self._regenerate.load()

        return self._regenerate(*args, **kwds)


def find_available_options():
    for ep in pkg_resources.iter_entry_points(group='pkglts'):
        option_name = ep.name.split(".")[0]
        if option_name not in available_options:
            available_options[option_name] = Option()

        opt = available_options[option_name]
        opt.from_entry_point(ep)


def get_user_permission(action_name, default_true=True):
    if default_true:
        return loc_input("%s [y], n?" % action_name) in ("", "y")
    else:
        return loc_input("%s y, [n]?" % action_name) == "y"

#
# def get_key(key, env):
#     """ Fetch a specific key in env
#     """
#     try:
#         elms = key.split(".")
#         d = env
#         for k in elms:
#             d = d[k]
#
#         return d
#     except KeyError:
#         return None
#
#
# def _ask_single_arg(name, default):
#     # prompt user for value
#     msg = name
#     if default is None:
#         msg += ":"
#         val = ""
#     else:
#         val = str(default)
#         msg += " [%s]:" % val
#
#     ans = loc_input(msg)
#     if ans == "":
#         return val
#     else:
#         return ans
#
#
# def ask_arg(name, pkg_cfg=None, default=None, extra=None):
#     """ Prompt the user for the value of some argument
#
#     If user returns nothing then default will be returned
#
#     If pkg_cfg is provided, the function will attempt to
#     find a proper default in it.
#
#     If extra is provided, the function will attempt to
#     find a value in it and return it without prompting
#     the user.
#
#     If default is a list of elements, even empty, the function
#     will return a list of answers.
#
#     args:
#      - name (str): name of argument. Can be in the form of
#                    'option.arg'.
#      - pkg_cfg (dict of (str, any)): place to look for defaults
#      - default (any): default to use as a last resort
#      - extra (dict of (str, any)): place to look for values
#
#     return:
#      - (str): value of argument either from prompt or from default
#     """
#     if extra is None:
#         extra = {}
#
#     # try to find value in extra
#     if name in extra:
#         return extra[name]
#
#     key = name.split(".")[-1]
#     if key in extra:
#         return extra[key]
#
#     if pkg_cfg is None:
#         pkg_cfg = {}
#
#     if isinstance(default, (list, tuple)):
#         # ask multiple args
#         val = get_key(name, pkg_cfg)
#         if val is None:
#             val = default
#
#         if not isinstance(val, (list, tuple)):
#             msg = "bad value in pkg_cfg, expected list for %s" % name
#             raise UserWarning(msg)
#
#         i = 0
#         items = []
#         res = "txt"
#         while res != "":
#             if i < len(val):
#                 loc_val = val[i]
#             else:
#                 loc_val = ""
#             res = _ask_single_arg(name, loc_val)
#             if res != "":
#                 items.append(res)
#                 i += 1
#
#         return items
#     else:
#         val = get_key(name, pkg_cfg)
#         if val is None:
#             val = default
#         return _ask_single_arg(name, val)
