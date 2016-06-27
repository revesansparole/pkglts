from base64 import b64encode
from hashlib import sha512
import json
import logging
from os.path import join as pj
from os.path import normpath

from .config import pkglts_dir, pkg_hash_file
from .templating import parse_source


logger = logging.getLogger(__name__)


def pth_as_key(pth):
    """Normalize path to enable to use them as keys

    Args:
        pth (str):

    Returns:
        (str)
    """
    return normpath(pth).replace("\\", "/")


def compute_hash(txt):
    """Compute hash summary of a text

    Args:
        txt:

    Returns:

    """
    algo = sha512()
    algo.update(txt.encode('utf-8'))  # TODO bad if non utf-8 encoded file
    return b64encode(algo.digest()).decode('utf-8')


def get_pkg_hash(rep="."):
    """Read pkg_hash file associated to this package

    Args:
        rep (str): directory to search for info

    Returns:
        (dict of str: list): hash map of preserved sections in this
                             package
    """
    with open(pj(rep, pkglts_dir, pkg_hash_file), 'r') as f:
        hm = json.load(f)

    return hm


def write_pkg_hash(pkg_hash, rep="."):
    """Store hash associated to this package on disk.

    Args:
        pkg_hash (dict of str: list): hash map of preserved sections in this
                                     package
        rep (str): directory to search for info

    Returns:
        None
    """
    logger.info("write package hash")
    cfg = dict(pkg_hash)

    with open(pj(rep, pkglts_dir, pkg_hash_file), 'w') as f:
        json.dump(cfg, f, sort_keys=True, indent=2)


def modified_file_hash(pth, pkg_hash):
    """Check whether a file complies with previously stored hash

    Args:
        pth (str): path to file to test
        pkg_hash (dict of str: list): hash map of preserved sections in this
                                     package

    Returns:
        (bool): whether this file has been modified or not
    """
    ref_blocks = pkg_hash[pth_as_key(pth)]

    with open(pth, 'r') as f:
        blocks = parse_source(f.read())

    lts_blocks = dict((bid, cnt) for bid, bef, cnt, aft in blocks
                      if bid is not None)
    if set(lts_blocks) != set(ref_blocks):
        return True
    else:
        for bid, cnt in lts_blocks.items():
            sha = compute_hash(cnt)
            if sha != ref_blocks[bid]:
                return True
