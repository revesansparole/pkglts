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


def pkg_full_name(txt, env):
    del txt  # unused
    namespace = env['base']['namespace']
    if namespace is None:
        return env['base']['pkgname']
    else:
        return namespace + "." + env['base']['pkgname']


mapping = {'upper': upper,
           'lower': lower,
           "base.src_pth": get_src_pth,
           "base.pkg_full_name": pkg_full_name}
