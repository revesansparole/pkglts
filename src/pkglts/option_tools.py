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


def empty_list(*args):
    return []


def empty_dict(*args):
    return {}


class Option(object):
    """Base class to store information associated with an option
    """

    def __init__(self):
        self.parameters = []
        self.check = empty_list
        self.require = empty_list
        self.environment_extensions = empty_dict
        self.regenerate = empty_list

    def from_entry_point(self, ep):
        func_name = ep.name.split(".")[-1]
        if func_name == "parameters":
            self.parameters = ep.load()
        elif func_name == "check":
            self.check = ep.load()
        elif func_name == "require":
            self.require = ep.load()
        elif func_name == "environment_extensions":
            self.environment_extensions = ep.load()
        elif func_name == "regenerate":
            self.regenerate = ep.load()
        else:
            # silently ignore other type of entry points
            logger.error("unknown entry point attribute: '{}'".format(func_name))


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
