from pkglts.local import pkg_full_name, src_dir


def environment_extensions(env):
    """Add more functionality to an environment.

    Args:
        env (jinja2.Environment):

    Returns:
        dict of str: any
    """
    return {"pkg_full_name": pkg_full_name(env),
            "src_pth": src_dir(env)}
