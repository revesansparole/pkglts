""" Templating tools
"""


class Node(object):
    """ Local class created to parse files
    """
    def __init__(self, typ, parent):
        self.typ = typ
        self.key = None
        self.parent = parent
        self.children = []
        self.data = []

        if parent is not None:
            parent.children.append(self)


def parse(txt):
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
            cur_node = Node("txt", div_node)
            i += 2

            # find key
            ind = txt[i:].find(",")
            div_node.key = txt[i:][:ind]
            i += ind + 1
            if txt[i] == " ":
                i += 1  # strip space after comma
        elif txt[i] == "}" and txt[i + 1] == "}":
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


def div_replace(parent, handlers, env):
    """ Reconstruct the whole text inside the text
    attribute of the node and return a version
    of it transformed according to the class attribute.

    args:
     - parent (Node): current node to explore
     - handlers (dict of (str: handler)): map of key handlers to use
     - env (dict of (str: dict)): extra info to pass to handlers

    return:
     - (str): newly formatted text
    """
    txt = ""
    for node in parent.children:
        if node.typ == 'txt':
            node_txt = "".join(node.data)
            # print "node txt", node_txt
            if len(node_txt) > 0:
                # check for '#' character before the end
                test_txt = node_txt.rstrip()
                if len(test_txt) > 0 and test_txt[-1] == '#':
                    test_txt = test_txt[:-1]
                    if len(test_txt) > 0 and test_txt[-1] == '\n':
                        test_txt = test_txt[:-1]

                    node_txt = test_txt
                txt += node_txt
        else:  # by construction it must be a div node
            txt += div_replace(node, handlers, env)
        # elif node.typ == 'div':
        #     txt += div_replace(node, handlers, env)
        # else:
        #     raise UserWarning("unrecognized type of node")

    handler = get_handler(parent.key, handlers)
    # print "handler", handler
    # print "txt", txt
    return handler(txt, env)


def replace(txt, handlers, env):
    """ Parse a txt for div elements and reconstruct it
    handling the txt inside the div elements if necessary.

    args:
     - txt (str): current txt to explore
     - handlers (dict of (str: handler)): map of key handlers to use
     - env (dict of (str: dict)): extra info to pass to handlers

    return:
     - (str): newly formatted text
    """
    root = parse(txt)
    txt = div_replace(root, handlers, env)
    return txt
