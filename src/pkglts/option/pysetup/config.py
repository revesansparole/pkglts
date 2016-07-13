parameters = [
    ("intended_versions", ["27"]),
    ("require", [])
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    intended_versions = env.globals['pysetup'].intended_versions

    if len(intended_versions) == 0:
        invalids.append("intended_versions")

    require = env.globals['pysetup'].require

    valid_methods = (None, "pip", "conda", "git")
    if any(imeth not in valid_methods for imeth, name in require):
        invalids.append("require")

    return invalids
