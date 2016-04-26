from base64 import b64encode
from hashlib import sha512

from .templating import flatten_divs, get_comment_marker, parse


def write_file(pth, content):
    """Write the content of a file on a local path and
    register associated hash for further modification
    tests.

    Args:
        pth (str): path to the new created file
        content (str): content to write on disk

    Returns:

    """
    """

    args:
     - pth (str): path to the new created file
     - content (str): content to write on disk
    """
    with open(pth, 'wb') as f:
        f.write(content.encode("utf-8"))


def _get_div_txt(node):
    if node.typ == "txt":
        return "".join(node.data)
    else:
        return "".join(_get_div_txt(child) for child in node.children)


def get_hash(pth):
    """Compute hash associated to a file.

    Actually compute hash of each pkglts section in file only

    Args:
        pth (str): path to file to analyse

    Returns:
        hash (list of str): one hash per pkglts section
    """
    with open(pth, 'r') as f:
        content = f.read()

    root = parse(content, get_comment_marker(pth))

    hm = []
    for div in flatten_divs(root):
        if div.key.split(" ")[0] == 'pkglts':
            algo = sha512()
            algo.update("".join(_get_div_txt(div)).encode('utf-8'))  # TODO bad if non utf-8 encoded file
            hm.append(b64encode(algo.digest()).decode('utf-8'))

    return tuple(hm)
