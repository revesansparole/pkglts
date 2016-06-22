from pkglts.option.doc import fmt_badge


def badge(txt, env):
    del txt  # unused
    project = env['readthedocs']['project']
    project = project.replace(".", "")
    url = "%s.readthedocs.io/en/latest/?badge=latest" % project
    img = "readthedocs.org/projects/%s/badge/?version=latest" % project
    return fmt_badge(img, url, "Documentation status")


mapping = {'readthedocs.badge': badge}


def environment_extensions(env):
    """Add more functionality to an environment.

    Args:
        env (jinja2.Environment):

    Returns:
        dict of str: any
    """
    project = env.globals['readthedocs'].project
    project = project.replace(".", "")
    url = "%s.readthedocs.io/en/latest/?badge=latest" % project
    img = "readthedocs.org/projects/%s/badge/?version=latest" % project
    badge = fmt_badge(img, url, "Documentation status")

    return {"badge": badge}
