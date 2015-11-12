from pkglts.local import src_dir


def upper(txt, env):
    del env  # unused
    return txt.upper()


def lower(txt, env):
    del env  # unused
    return txt.lower()


def get_src_pth(txt, env):
    del txt  # unused
    return src_dir(env)


mapping = {'upper': upper,
           'lower': lower,
           "src_pth": get_src_pth}
