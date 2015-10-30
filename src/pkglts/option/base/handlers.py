from pkglts.local import src_dir


def upper(txt, env):
    return txt.upper()


def lower(txt, env):
    return txt.lower()


def get_src_pth(txt, env):
    return src_dir(env)


mapping = {'upper': upper,
           'lower': lower,
           "src_pth": get_src_pth}
