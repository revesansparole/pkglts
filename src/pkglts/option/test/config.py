parameters = [
    ("suite_name", "pytest")
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    name = env.globals['test'].suite_name

    if name not in ("pytest", "nose"):
        invalids.append('suite_name')

    return invalids
