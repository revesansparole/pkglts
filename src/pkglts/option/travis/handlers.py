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

    url = "travis-ci.org/%s/%s" % (owner, project)
    img = url + ".svg?branch=master"
    badge = fmt_badge(img, url, "Travis build status")

    return {"badge": badge}
