
parameters = [
    ("theme", 'default')
]


def check(pkg_cfg):
    """Check the validity of parameters in package configuration.

    Args:
        pkg_cfg (dict of str, dict of str, any)): package configuration

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    theme = pkg_cfg['sphinx']['theme']
    if theme != str(theme):
        invalids.append('theme')

    return invalids
