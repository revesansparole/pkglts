parameters = [
    ("major", 0),
    ("minor", 1),
    ("post", 0)
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

    if not isinstance(major, int):
        invalids.append("major")
    if not isinstance(minor, int):
        invalids.append("minor")
    if not isinstance(post, int):
        invalids.append("post")

    return invalids
