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

    url = "coveralls.io/github/%s/%s?branch=master" % (owner, project)
    img = ("coveralls.io/repos/github/%s/%s/" % (owner, project) +
           "badge.svg?branch=master")
    badge = fmt_badge(img, url, "Coverage report status", cfg['doc']['fmt'])

    return {"badge": badge}
