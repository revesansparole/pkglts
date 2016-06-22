parameters = [
    ("intended_versions", ["27"])
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

    return invalids
