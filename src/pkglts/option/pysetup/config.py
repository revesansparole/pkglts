parameters = [
    ("author_name", "{{key, base.owner}}"),
    ("author_email", "moi@email.com"),
    ("intended_versions", ["27"])
]


def check(pkg_cfg):
    """Check the validity of parameters in package configuration.

    args:
     - pkg_cfg (dict of str, dict of str, any)): package configuration

    return:
     - (list of str): list of faulty parameters
    """
    invalids = []
    cfg = pkg_cfg['pysetup']
    author_name = cfg['author_name']
    intended_versions = cfg['intended_versions']

    if len(author_name) == 0:
        invalids.append("author_name")
    if len(intended_versions) == 0:
        invalids.append("intended_versions")

    return invalids
