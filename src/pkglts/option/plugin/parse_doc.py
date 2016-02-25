import re
from sphinx.util.docstrings import prepare_docstring


def parse_docstring(txt):
    """Extract components of a google formatted docstring

    Args:
        txt: (str) actual docstring to parse

    Returns:
        (dict of (str, val)) mapping of docstring sections
    """
    doc = [line.rstrip() for line in prepare_docstring(txt) if len(line.strip()) > 0]

    parsed = dict(caption="", doc=[], args={}, returns=None)

    arg_pattern = re.compile(r"""
    ^(?P<name>\w+)       # param name
    (:[ ]*               # rest is optional (only param name)
    (                    # param type is optional
    \((?P<type>\w+)\)    # param type
    )?                   # optional param type
    [ ]*(?P<descr>.+$)?  # param description consume the rest of the line
    )?                   # case of only param name
    """, re.VERBOSE)

    ret_pattern = re.compile(r"""
    ^((?P<name>\w+):[ ]*)?      # return name is optional
    \((?P<type>\w+)\)    # return type
    [ ]*(?P<descr>.+$)?  # return description consume the rest of the line
    """, re.VERBOSE)

    state = ["top"]
    for line in doc:
        if line.startswith("Args:"):
            if state[-1] != "top":
                state.pop(-1)

            state.append("args")
        elif line.startswith("Returns:"):
            if state[-1] != "top":
                state.pop(-1)

            state.append("returns")
        else:
            if state[-1] == "top":
                if parsed['caption'] == "":
                    parsed['caption'] = line
                else:
                    parsed['doc'].append(line)
            elif state[-1] == "args":
                if line[0] != " ":
                    state.pop(-1)
                    parsed['doc'].append(line)
                else:
                    match = re.match(arg_pattern, line.lstrip())
                    parsed['args'][match.group('name')] = (match.group('type'),
                                                           match.group('descr'))
            elif state[-1] == "returns":
                if line[0] != " ":
                    state.pop(-1)
                    parsed['doc'].append(line)
                else:
                    match = re.match(ret_pattern, line.lstrip())
                    parsed['returns'] = (match.group('name'),
                                        match.group('type'),
                                        match.group('descr'))
            else:
                raise UserWarning("how did we even reach this point?")

    return parsed
