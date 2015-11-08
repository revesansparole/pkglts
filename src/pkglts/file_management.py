from base64 import b64encode
from hashlib import sha512

from .templating import flatten_divs, get_comment_marker, parse


def write_file(pth, content):
    """ Write the content of a file on a local path and
    register associated hash for further modification
    tests.

    args:
     - pth (str): path to the new created file
     - content (str): content to write on disk
    """
    with open(pth, 'wb') as f:
        f.write(content.encode("utf-8"))


def get_div_txt(node):
    if node.typ == "txt":
        return "".join(node.data)
    else:
        return "".join(get_div_txt(child) for child in node.children)


def get_hash(pth):
    """ Compute hash associated to a file.

    If file can be modified by user, hash will be computed
    for each pkglts div inside content.
    Else total content will be used.

    args:
     - pth (str): path to file to analyse
     - editable (bool): default False, whether the file can be modified
                        by user or not

    return:
     - hash (str): hash created from the content of the file
    """
    with open(pth, 'r') as f:
        content = f.read()

    root = parse(content, get_comment_marker(pth))

    hm = []
    for div in flatten_divs(root):
        if div.key.split(" ")[0] == 'pkglts':
            algo = sha512()
            algo.update("".join(get_div_txt(div)).encode('utf-8'))  # TODO bad if non utf-8 encoded file
            hm.append(b64encode(algo.digest()).decode('utf-8'))

    return tuple(hm)
