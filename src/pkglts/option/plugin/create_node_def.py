from funcsigs import signature
from uuid import uuid1


def create_node_def(func):
    """Create a node definition schema for the given function

    Args:
        func: (function) actual function object

    Returns:
        (dict): schema as specified in node/schema
    """
    node_def = dict(id=uuid1().hex,
                    name=func.__name__,
                    description=func.__doc__,
                    author="unknown",
                    version=0,
                    function="%s:%s" % (func.__module__, func.__name__),
                    inputs=[],
                    outputs=[])

    s = signature(func)
    for pname, p in s.parameters.items():
        port = dict(name=pname, interface="IAny", description="")
        if p.default != p.empty:
            port["default"] = str(p.default)
        node_def['inputs'].append(port)

    return node_def
