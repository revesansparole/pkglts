parameters = [
    ("description", "belle petite description"),
    ("keywords", [])
]


def check(pkg_cfg):
    """Check the validity of parameters in package configuration.

    args:
     - pkg_cfg (dict of str, dict of str, any)): package configuration

    return:
     - (list of str): list of faulty parameters
    """
    invalids = []
    description = pkg_cfg['doc']['description']
    # keywords = pkg_cfg['doc']['keywords']

    if len(description) == 0:
        invalids.append("description")

    return invalids
