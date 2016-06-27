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

    url = "coveralls.io/github/%s/%s?branch=master" % (owner, project)
    img = ("coveralls.io/repos/github/%s/%s/" % (owner, project) +
           "badge.svg?branch=master")
    badge = fmt_badge(img, url, "Coverage report status")

    return {"badge": badge}
