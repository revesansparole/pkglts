
parameters = [
    ("theme", 'default'),
    ("autodoc_dvlpt", True)
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    theme = env.globals['sphinx'].theme
    if theme != str(theme):
        invalids.append('theme')

    return invalids
