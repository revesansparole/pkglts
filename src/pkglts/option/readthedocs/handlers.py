from pkglts.option.doc import fmt_badge


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    project = cfg['readthedocs']['project']
    project = project.replace(".", "")
    url = "%s.readthedocs.io/en/latest/?badge=latest" % project
    img = "readthedocs.org/projects/%s/badge/?version=latest" % project
    badge = fmt_badge(img, url, "Documentation status", cfg['doc']['fmt'])

    return {"badge": badge}
