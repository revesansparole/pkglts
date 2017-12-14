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

    base_url = "requires.io/github/%s/%s/" % (owner, project)
    url = base_url + "requirements/?branch=master"
    img = base_url + "requirements.svg?branch=master"
    badge = fmt_badge(img, url, "Requirements status", cfg['doc']['fmt'])

    return {"badge": badge}
