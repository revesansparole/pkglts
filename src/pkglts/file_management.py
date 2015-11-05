from base64 import b64encode
from hashlib import sha512
from os import mkdir

from .templating import flatten_divs, get_comment_marker, parse


# def get_revision(txt):
#     """ Get file revision as defined locally by a single statement
#     # rev =
#     on a single line
#
#     args:
#      - txt (str): text content to parse
#     """
#     for line in txt.splitlines():
#         if line.startswith("# rev = "):
#             return int(line[8:].strip())
#
#     return None


# def make_dir(pth, hashmap=None):
#     """ Create a new directory and register it in
#     hash map for later checks
#
#     args:
#      - pth (str): path to new created directory
#      - hashmap (dict of (str: sha512)): mapping between
#                  file path and hash keys. If None, simply
#                  create dir on disk.
#     """
#     mkdir(pth)
#
#     if hashmap is not None:
#         hashmap[pth] = "walou"


def write_file(pth, content, hashmap=None):
    """ Write the content of a file on a local path and
    register associated hash for further modification
    tests.

    args:
     - pth (str): path to the new created file
     - content (str): content to write on disk
     - hashmap (dict of (str: sha512)): mapping between
                 file path and hash keys. If None, simply
                 write file on disk.
    """
    with open(pth, 'wb') as f:
        f.write(content.encode("utf-8"))

    # if hashmap is not None:
    #     algo = sha512()
    #     algo.update(content.encode("utf-8"))
    #     hashmap[pth] = b64encode(algo.digest()).decode("utf-8")


# def user_modified(pth, hashmap):
#     """ Check whether the file has been tempered by user
#     according to a stored hash.
#
#     args:
#      - pth (str): full path to the file
#      - hashmap (dict of pth: sha512): table of hash keys
#
#     return:
#      - False: if file do not have a hash or if stored hash
#               is different equal stored one
#      - True: if file hash is different from stored one
#     """
#     if pth not in hashmap:
#         return True
#
#     ref_hash = hashmap[pth]
#
#     algo = sha512()
#     with open(pth, 'rb') as f:
#         content = f.read()
#         algo.update(content)
#
#     new_hash = b64encode(algo.digest()).decode("utf-8")
#     return new_hash != ref_hash


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
