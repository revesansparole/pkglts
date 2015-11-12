def get_extra(txt, env):
    """ Get extra ignore items
    """
    del env  # unused
    try:
        with open(".gitignore.extra", 'r') as f:
            txt = f.read()

        return txt
    except IOError:
        pass

    return txt


mapping = {'git.ignore': get_extra}
