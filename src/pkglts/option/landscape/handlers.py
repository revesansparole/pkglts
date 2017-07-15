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

    url = "landscape.io/github/%s/%s/master" % (owner, project)
    img = url + "/landscape.svg?style=flat"
    badge = fmt_badge(img, url, "Code health status")

    return {"badge": badge}
