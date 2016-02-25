from importlib import import_module
from inspect import isfunction
import json
from os.path import exists, splitext
from pkgutil import walk_packages

from pkglts.local import pkg_full_name

from create_node_def import create_node_def


def find_plugin_categories(txt):
    if txt is None:
        return []

    if '__plugin__' not in txt:
        return []

    for line in txt.splitlines():
        if '__plugin__' in line:
            cat_txt = line.strip().split(":")[1].strip()
            return [c.strip() for c in cat_txt.split(",")]


def parse_plugins(pkg):
    """Parse recursively all plugins in a given package

    Notes: write plugin def files

    Args:
        pkg: (Package) a python package object

    Returns:
        None
    """
    for imp, modname, ispkg in walk_packages(pkg.__path__):
        loader = imp.find_module(modname)
        mod = import_module("%s.%s" % (pkg.__name__, loader.fullname))
        if ispkg:
            parse_plugins(mod)
        else:
            plugins = {}
            if hasattr(mod, '__all__'):
                item_names = mod.__all__
            else:
                item_names = dir(mod)
            for item_name in item_names:
                item = getattr(mod, item_name)
                if isfunction(item):
                    for cat in find_plugin_categories(item.__doc__):
                        if cat == "node":
                            plugins[item_name] = create_node_def(item)

            if len(plugins) > 0:
                root_pth = splitext(mod.__file__)[0]
                for item_name, idef in plugins.items():
                    pth = "%s_%s.json" % (root_pth, item_name)
                    if exists(pth):
                        with open(pth, 'r') as f:
                            old_idef = json.load(f)

                        idef['id'] = old_idef['id']

                    with open(pth, 'w') as f:
                        json.dump(idef, f, indent=2)


def main(pkg_cfg):
    """Main function called to walk the package

    Args:
        pkg_cfg: (dict of (str, dict)) package configuration parameters
    """
    pkg = import_module(pkg_full_name(pkg_cfg))
    parse_plugins(pkg)
