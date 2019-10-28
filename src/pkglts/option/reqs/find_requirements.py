"""
This tool will display all dependencies used by this package.
"""
import ast
import logging
from glob import glob
from os import path

from pkglts.local import src_dir

LOGGER = logging.getLogger(__name__)

stdpkgs = set(line.strip() for line in open(path.join(path.dirname(__file__), "stdpkgs.txt")).readlines()
              if len(line.strip()) > 0 and not line.startswith("#"))


def iter_ext_imports(body):
    for node in body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:  # only external imports
                yield node.module

        # elif isinstance(node, ast.FunctionDef):
        #     for name, level in iter_imports(node.body):
        #         yield name, level


def find_reqs(pth):
    """Find all requirements (imports) used by a script.

    Args:
        pth (str): path to file to parse

    Returns:
        (list): list of package names
    """
    src = open(pth, 'rb').read()
    pt = ast.parse(src, pth)
    # TODO pb with namespaces
    pkgs = set(pkgname.split(".")[0] for pkgname in iter_ext_imports(pt.body))

    return pkgs


def action_find_reqs(cfg, **kwds):
    """Find dependencies used by this package.
    """
    LOGGER.info("Find requirements")
    this_pkgname = cfg['base']['pkgname']

    for dirpth in (src_dir(cfg), 'doc', 'example', 'script', 'test'):
        if path.exists(dirpth):
            print("############\n# %s\n############" % dirpth)
            reqs = set()
            for pth in glob("%s/*.py" % dirpth) + glob("%s/**/*.py" % dirpth):
                if not path.basename(pth).startswith("_"):
                    reqs.update(find_reqs(pth))
            reqs -= {this_pkgname}
            print("standard", sorted(reqs & stdpkgs))
            print("external", sorted(reqs - stdpkgs))
            print("")


def parser_find_reqs(subparsers):
    """Associate a CLI to this tool.

    Notes: The CLI will be a subcommand of pmg.

    Args:
        subparsers (ArgumentParser): entity to create a subparsers

    Returns:
        (string): a unique id for this parser
        (callable): the action to perform
    """
    subparsers.add_parser('reqs', help=action_find_reqs.__doc__)

    return 'reqs', action_find_reqs
