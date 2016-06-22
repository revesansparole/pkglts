parameters = [
    ("description", "belle petite description"),
    ("keywords", [])
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    description = env.globals['doc'].description
    # keywords = env.globals['doc'].keywords

    if len(description) == 0:
        invalids.append("description")

    return invalids
