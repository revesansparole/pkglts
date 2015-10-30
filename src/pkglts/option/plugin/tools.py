import __builtin__
from collections import OrderedDict
from inspect import getmembers, getmodule, isclass
from os import chdir, getcwd, mkdir, walk
from os.path import abspath, dirname, exists, normpath, sep, splitext
from string import Template
import sys

from pkglts.local import src_dir


def plugin_dir(pkg_cfg):
    return "src/%s_plugin" % pkg_cfg['base']['pkgname']


def discover_plugin(root, filename):
    """ Find all defined plugins in the given file.

    args:
     - root (str): path to a directory containing filename
     - filename (str): name of a python file containing plugin definitions
                       located in root.

    return:
     - (list of (str, str)): list of plugin name, plugin group
    """
    mem_dir = getcwd()
    chdir(root)
    sys.path.insert(0, root)

    # evaluate file
    with open(filename, 'r') as f:
        pycode = f.read()

    ast = compile(pycode, filename, 'exec')

    d = OrderedDict()
    eval(ast, d)
    # del d['__builtins__']

    plugins = []
    for name, obj in d.items():
        mod = getmodule(obj)
        if mod is None or (isclass(obj) and mod == __builtin__):
            # i.e. object defined in this file
            mbs = dict(getmembers(obj))
            if '__plugin__' in mbs:
                plugins.append((name, mbs['__plugin__']))

    chdir(mem_dir)
    del sys.path[0]

    return plugins


def get_definition_id(root, pth, obj_name):
    """ Construct a python identifier for reconstructing
    the given object.

    args:
     - root (str): base path for package
     - pth (str): absolute path to the definition file of the object
     - obj_name (str): object name as defined in the file

    return:
     - (str): 'pkg.module:obj_name' such as 'from pkg.module import obj_name'
              is a valid statement.
    """
    root = dirname(normpath(abspath(root)))
    pth = normpath(abspath(pth))
    assert pth.startswith(root)

    mod_pth = pth[(len(root) + 1):].split(sep)
    mod_pth[-1] = splitext(mod_pth[-1])[0]
    return ".".join(mod_pth) + ":" + obj_name


def find_plugins(pkg_dir):
    """ Walk recursively down the given directory
    to find all defined plugins.

    args:
     - pkg_dir (str): base directory of arborescence to explore

    return:
     - dict of (str: list of str): map of group name: list of plugin definition
                                  id.
    """
    for root, dnames, fnames in walk(pkg_dir):
        for name in fnames:
            if splitext(name)[1] == ".py":
                plugins = discover_plugin(abspath(root), name)
                if len(plugins) > 0:
                    pth = root + "/" + name
                    # remove pkg_dir from pth
                    pth = pth[(len(pkg_dir) + 1):]  # TODO better way
                    pth = pth.replace("\\", "/")
                    yield pth, plugins

# will be changed for some openalea.Plugin call hopefully
# plugin_tpl = Template("""
# class $object_name(object):
#     name = None
#     tags = None
#
#     def __call__(self):
#         from $package import $object
#         return $object()
# """)
plugin_tpl = Template("""
def $object_name():
    from $package import $object
    return $object()

$object_name.name = None
$object_name.tags = None
""")


def refresh_plugin_cache(pkg_cfg):
    """ Find all plugins in the package and create
    a cache for them in a src/pkg_plugin directory.
    """
    plugin_root = plugin_dir(pkg_cfg)
    entry_point = {}

    # discover all plugins in src/pkgname
    pkg_dir = src_dir(pkg_cfg)
    created_files = set()
    for pth, plugins in find_plugins(pkg_dir):
        print("pth", pth)
        print(plugins)

        # create new entries in src/pkgname_plugin if necessary
        plugin_pth = plugin_root + "/" + pth
        created_files.add(pth)
        if exists(plugin_pth):  # check definitions inside already existing file
            pass
        else:
            pth_dirs = [dirname(plugin_pth)]
            while dirname(pth_dirs[-1]) != "":
                pth_dirs.append(dirname(pth_dirs[-1]))

            for dpth in reversed(pth_dirs):
                if not exists(dpth):
                    mkdir(dpth)

                if not exists(dpth + "/" + "__init__.py"):
                    with open(dpth + "/" + "__init__.py", 'w') as f:
                        f.close()

            # if not exists(pth_dir): # TODO add __init__.py
            #     makedirs(pth_dir)
            with open(plugin_pth, 'w') as f:
                items = []
                for name, gr in plugins:
                    # obj_name = "Plugin%s" % name.capitalize()
                    obj_name = "func_%s" % name
                    pkg = splitext(pth.replace("/", "."))[0]
                    package = pkg_cfg['base']['pkg_fullname'] + "." + pkg
                    items.append(plugin_tpl.substitute(object_name=obj_name,
                                                       package=package,
                                                       object=name))

                    # add entry to entry points list
                    if gr not in entry_point:
                        entry_point[gr] = []

                    entry_point[gr].append((name, plugin_pth, obj_name))

                f.write("\n\n".join(items))

    # remove unused files
    existing_files = set()
    for root, dnames, fnames in walk(plugin_root):
        pass

    for pth in existing_files - created_files:
        print("remove file: %s" % pth)

    # return entry_points
    return entry_point
