from funcsigs import signature
from inspect import getsource
from uuid import uuid1

from parse_doc import parse_docstring


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
    pycode = getsource(func)
    print "pycode", pycode
    parsed = parse_docstring(func.__doc__)
    for pname, p in s.parameters.items():
        if pname in parsed['args']:
            arg_type, descr = parsed['args']

        if p.annotation == p.empty:
            interface = arg_type
            if interface is None:
                interface = "IAny"
        else:
            interface = str(p.annotation)

        if descr is None:
            description = ""
        else:
            description = str(descr)

        port = dict(name=pname, interface=interface, description=description)
        if p.default != p.empty:
            port["default"] = str(p.default)
        node_def['inputs'].append(port)

    if "return" in pycode:

        if parsed['returns'] is not None:
            ret_name, ret_type, ret_descr = parsed['returns']
            if ret_name is None:
                ret_name = "ret"

            if s.return_annotation == s.empty:
                if ret_type is None:
                    interface = "IAny"
                else:
                    interface = ret_type
            else:
                interface = str(s.return_annotation)

            if ret_descr is None:
                description = ""
            else:
                description = str(ret_descr)

            port = dict(name=ret_name,
                        interface=interface,
                        description=description)

            node_def['outputs'].append(port)

    return node_def
