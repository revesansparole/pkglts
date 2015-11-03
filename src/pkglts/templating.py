""" Templating tools
"""
from os.path import splitext


class Node(object):
    """ Local class created to parse files
    """
    def __init__(self, typ, parent):
        self.typ = typ
        self.key = None
        self.parent = parent
        self.children = []
        self.data = []
        self.pre_fmt = ""
        self.post_fmt = ""

        if parent is not None:
            parent.children.append(self)


space_chars = (" ", "\t", "\n")


def end_with_comment(data, comment_marker):
    nb = len(comment_marker)
    if len(data) >= nb:
        test = "".join(data[-nb:])
        return test == comment_marker
    else:
        return False


def find_fmt_chars(node, comment_marker):
    """ Consume all characters in node.data up to a comment marker

    returns:
      - (str): string of consumed characters
    """
    nb = len(comment_marker)
    fmt = []
    has_marker = False
    cont = True
    while cont and len(node.data) > 0:
        if end_with_comment(node.data, comment_marker):
            has_marker = True
            for s in comment_marker:
                fmt.insert(0, node.data[-1])
                del node.data[-1]
        elif node.data[-1] in space_chars:
            fmt.insert(0, node.data[-1])
            del node.data[-1]
        else:
            cont = False

    if has_marker:
        return "".join(fmt)
    else:
        node.data.extend(fmt)
        return ""


def parse(txt, comment_marker):
    """ Parse a text for '{{class, bla }}' sections
    and construct a tree of nested sections
    """
    root = Node("root", None)
    root.key = ""
    cur_node = Node("txt", root)

    i = 0
    while i < len(txt):
        if txt[i] == "{" and txt[i + 1] == "{":
            div_node = Node("div", cur_node.parent)
            div_node.pre_fmt = find_fmt_chars(cur_node, comment_marker)

            cur_node = Node("txt", div_node)
            i += 2

            # find key
            ind = txt[i:].find(",")
            div_node.key = txt[i:][:ind]
            i += ind + 1
            if txt[i] == " ":
                i += 1  # strip space after comma
        elif txt[i] == "}" and ((i + 1) < len(txt) and txt[i + 1] == "}"):  # TODO potential trouble if text finish with single }
            cur_node.parent.post_fmt = find_fmt_chars(cur_node, comment_marker)
            cur_node = Node("txt", cur_node.parent.parent)
            i += 2
        else:
            cur_node.data.append(txt[i])
            i += 1

    return root


def same(txt, env):
    """ local function created to handle no class hooks
    """
    return txt


def remove(txt, env):
    """ Return empty string
    """
    return ""


def delete(txt, env):
    """ Return '_' string used by some function
    to recognize empty names
    """
    return "_"


def get_key(txt, env):
    """ Fetch a specific key in env
    """
    try:
        elms = txt.split(".")
        d = env
        for k in elms:
            d = d[k]

        return d
    except KeyError:
        return txt


loc_handlers = {'remove': remove,
                'rm': remove,
                'del': delete,
                'key': get_key}


def get_handler(key, handlers):
    """ Return an instance of a handler
    handler(txt, env) -> modified txt
    """
    all_hands = dict(loc_handlers)
    all_hands.update(handlers)
    for k in key.split(" "):
        if k in all_hands:
            return all_hands[k]

    return same


def div_replace(node, handlers, env, comment_marker):
    """ Reconstruct the whole text inside the text
    attribute of the node and return a version
    of it transformed according to the class attribute.

    args:
     - node (Node): current node to explore
     - handlers (dict of (str: handler)): map of key handlers to use
     - env (dict of (str: dict)): extra info to pass to handlers
     - comment_marker (str|re): characters used to mark inline comment

    return:
     - (str): newly formatted text
    """
    txt = ""
    for child in node.children:
        if child.typ == 'txt':
            txt += "".join(child.data)
        else:  # by construction it must be a div node
            txt += div_replace(child, handlers, env, comment_marker)

    # handle formatting
    if node.key.split(" ")[0] == "pkglts":
        pre = node.pre_fmt + "{{%s," % node.key
        if not txt.startswith("\n"):
            pre += " "
        post = node.post_fmt + "}}"
    else:
        if comment_marker in node.pre_fmt:
            if comment_marker in node.post_fmt:  # block div
                # remove pre and post formatting characters
                pre = ""
                post = ""
            else:  # inline div
                pre = node.pre_fmt[:node.pre_fmt.index(comment_marker)]
                post = ""
        else:
            pre = node.pre_fmt
            post = node.post_fmt

    handler = get_handler(node.key, handlers)
    return pre + handler(txt, env) + post


def replace(txt, handlers, env, comment_marker="#"):
    """ Parse a txt for div elements and reconstruct it
    handling the txt inside the div elements if necessary.

    args:
     - txt (str): current txt to explore
     - handlers (dict of (str: handler)): map of key handlers to use
     - env (dict of (str: dict)): extra info to pass to handlers
     - comment_marker (str|re): characters used to mark inline comment

    return:
     - (str): newly formatted text
    """
    root = parse(txt, comment_marker)
    txt = div_replace(root, handlers, env, comment_marker)
    return txt


def get_comment_marker(filename):
    """ Try to guess the characters used to signify comments
    in the given file.

    Based solely on the extension of filename.

    args:
     - filename (str): name used to infer type of marker

    return:
     - marker (str): string of characters used to mark inline comments
    """
    ext = splitext(filename)[1].lower()
    if ext == ".bat":
        return "REM "
    elif ext == ".ini":
        return "#"
    elif ext == ".py":
        return "#"
    elif ext == ".rst":
        return ".. "
    else:
        return "#"  # default
