from os.path import exists


parameters = [
    ("src_directory", "example")
]


def check(env):
    """Check the validity of parameters in working environment.

    Args:
        env (jinja2.Environment):  current working environment

    Returns:
        (list of str): list of faulty parameters
    """
    invalids = []
    src_directory = env.globals['notebook'].src_directory

    if not exists(src_directory):
        invalids.append("src_directory")

    return invalids
