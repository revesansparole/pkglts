from pkglts.option.doc import fmt_badge


def environment_extensions(env):
    """Add more functionality to an environment.

    Args:
        env (jinja2.Environment):

    Returns:
        dict of str: any
    """
    owner = env.globals['github'].owner
    project = env.globals['github'].project

    url = "landscape.io/github/%s/%s/master" % (owner, project)
    img = url + "/landscape.svg?style=flat"
    badge = fmt_badge(img, url, "Code health status")

    return {"badge": badge}
