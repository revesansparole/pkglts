parameters = [
    ("major", "0"),
    ("minor", "1"),
    ("post", "0")
]


def check(pkg_cfg):
    """Check the validity of parameters in package configuration.

    args:
     - pkg_cfg (dict of str, dict of str, any)): package configuration

    return:
     - (list of str): list of faulty parameters
    """
    invalids = []
    major = pkg_cfg['version']['major']
    minor = pkg_cfg['version']['minor']
    post = pkg_cfg['version']['post']

    try:
        int(major)
    except ValueError:
        invalids.append("major")
    try:
        int(minor)
    except ValueError:
        invalids.append("minor")
    try:
        int(post)
    except ValueError:
        invalids.append("post")

    return invalids
