from pkglts.option.doc import fmt_badge


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    owner = cfg['github']['owner']
    project = cfg['github']['project']

    url = "travis-ci.org/%s/%s" % (owner, project)
    img = url + ".svg?branch=master"
    badge = fmt_badge(img, url, "Travis build status")

    return {"badge": badge}
